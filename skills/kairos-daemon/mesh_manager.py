#!/usr/bin/env python3
"""
Mesh Manager v0.14 - Decentralized P2P sync and heartbeat for KAIROS
Uses a lightweight HTTP server for gossip/task sync.
Zero-dependency implementation using BaseHTTPRequestHandler.
"""

import os
import json
import time
import socket
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import request, error
from typing import List, Dict, Optional

class MeshRequestHandler(BaseHTTPRequestHandler):
    """Simple API for mesh gossip and task sync."""
    
    def log_message(self, format, *args):
        pass

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        response_data = {"status": "ok"}
        
        if self.path == "/mesh/ping":
            response_data["version"] = "0.14-mesh"
            response_data["node_id"] = self.server.mesh.node_id
            
        elif self.path == "/mesh/sync":
            response_data["tasks"] = self.server.mesh.daemon.queue.get_pending()
            
        elif self.path == "/mesh/push":
            task_text = data.get("task")
            if task_text:
                self.server.mesh.daemon.queue.add_task(f"[MESH:{data.get('from')}] {task_text}")
                response_data["message"] = "Task accepted into local queue"
        
        elif self.path == "/mesh/admin/add_peer":
            peer_addr = data.get("peer")
            if peer_addr:
                self.server.mesh.add_peer(peer_addr)
                response_data["message"] = f"Peer {peer_addr} added to mesh"
        
        elif self.path == "/mesh/admin/list_peers":
            response_data["peers"] = self.server.mesh.peers

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode('utf-8'))

class MeshManager:
    """Manages decentralized peer-to-peer synchronization."""

    def __init__(self, daemon, host="127.0.0.1", port=5000):
        self.daemon = daemon
        self.host = host
        self.port = port
        self.node_id = f"{host}:{port}"
        self.peers = {} # host:port -> {"last_seen": timestamp, "status": "online"}
        self.running = False
        self.server = None
        self.mesh_thread = None
        self.heartbeat_thread = None
        self.sync_interval = 10
        self.failover_threshold = 30

    def start(self):
        self.running = True
        self.server = HTTPServer((self.host, self.port), MeshRequestHandler)
        self.server.mesh = self
        self.mesh_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.mesh_thread.start()
        self.heartbeat_thread = threading.Thread(target=self._heartbeat_loop, daemon=True)
        self.heartbeat_thread.start()
        self.daemon._log(f"MeshManager v0.14 listening on {self.node_id}")

    def stop(self):
        self.running = False
        if self.server:
            self.server.shutdown()
        if self.mesh_thread:
            self.mesh_thread.join()

    def add_peer(self, peer_addr: str):
        if peer_addr != self.node_id and peer_addr not in self.peers:
            self.peers[peer_addr] = {"last_seen": 0, "status": "unknown"}
            self.daemon._log(f"Peer added: {peer_addr}")

    def get_peers(self) -> Dict:
        return self.peers

    def _heartbeat_loop(self):
        while self.running:
            for peer in list(self.peers.keys()):
                self._ping_peer(peer)
            time.sleep(self.sync_interval)

    def _ping_peer(self, peer: str):
        try:
            url = f"http://{peer}/mesh/ping"
            req = request.Request(url, method="POST", data=b'{}')
            with request.urlopen(req, timeout=2) as resp:
                data = json.loads(resp.read().decode())
                if data.get("status") == "ok":
                    self.peers[peer]["last_seen"] = time.time()
                    self.peers[peer]["status"] = "online"
                    if self.daemon.tick_count % 3 == 0:
                        self._sync_tasks_with_peer(peer)
        except Exception:
            if time.time() - self.peers[peer]["last_seen"] > self.failover_threshold:
                if self.peers[peer]["status"] == "online":
                    self.daemon._log(f"PEER FAILOVER: Node {peer} offline.")
                    self.peers[peer]["status"] = "offline"

    def _sync_tasks_with_peer(self, peer: str):
        try:
            url = f"http://{peer}/mesh/sync"
            req = request.Request(url, method="POST", data=b'{}')
            with request.urlopen(req, timeout=2) as resp:
                data = json.loads(resp.read().decode())
                peer_tasks = data.get("tasks", [])
                local_tasks = [t["task"] for t in self.daemon.queue.get_pending()]
                for pt in peer_tasks:
                    p_task = pt["task"]
                    if p_task not in local_tasks and "[MESH:" not in p_task:
                        self.daemon.queue.add_task(f"[MESH:{peer}] {p_task}")
        except Exception:
            pass

    def push_task_to_peers(self, task_text: str):
        for peer, info in self.peers.items():
            if info["status"] == "online":
                try:
                    data = json.dumps({"task": task_text, "from": self.node_id}).encode('utf-8')
                    url = f"http://{peer}/mesh/push"
                    req = request.Request(url, method="POST", data=data)
                    request.urlopen(req, timeout=2)
                except Exception:
                    pass

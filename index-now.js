const { google } = require('googleapis');
const fs = require('fs');

async function notifyGoogle() {
  try {
    // Read JSON key from environment variable (Secret)
    const keyData = process.env.GOOGLE_INDEXING_KEY;
    if (!keyData) {
      throw new Error('GOOGLE_INDEXING_KEY environment variable is missing');
    }
    
    const keys = JSON.parse(keyData);
    const jwtClient = new google.auth.JWT(
      keys.client_email,
      null,
      keys.private_key,
      ['https://www.googleapis.com/auth/indexing'],
      null
    );

    await jwtClient.authorize();

    const options = {
      url: 'https://indexing.googleapis.com/v3/urlNotifications:publish',
      method: 'POST',
      auth: jwtClient,
      data: {
        url: 'https://evansxm.github.io/evansmathibe-agency/',
        type: 'URL_UPDATED'
      }
    };

    const response = await google.indexing('v3').urlNotifications.publish(options);
    console.log('Indexing request sent successfully:', response.data);
  } catch (error) {
    console.error('Error notifying Google Indexing API:', error.message);
    process.exit(1);
  }
}

notifyGoogle();

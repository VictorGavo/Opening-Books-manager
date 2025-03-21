/**
 * Google Apps Script to send form data to a webhook
 * 
 * This script should be attached to both the SOD and EOD Google Forms.
 * It will send the form data to the webhook endpoint when a form is submitted.
 * 
 * To use this script:
 * 1. Open your Google Form in edit mode
 * 2. Click the three dots (⋮) in the top right corner
 * 3. Select "Script editor"
 * 4. Copy and paste this code
 * 5. Replace the WEBHOOK_URL with your server's webhook URL
 * 6. Save the script
 * 7. Set up a trigger for the onSubmit function to run when a form is submitted
 */

// Replace with your server's webhook URL
const WEBHOOK_URL = 'http://your-server-address:5000/webhook';

// Form IDs - these help identify which form was submitted
const SOD_FORM_ID = '1blTpEVqj9xASpwgPJLATF65uiPImf3EME8AEHg2AWhE';
const EOD_FORM_ID = '1TyIrAUBNUZeiJLg04Y10JqDAQF8m3Li3Sa6w9RJK6ZQ';

/**
 * Handles form submission event
 */
function onSubmit(e) {
  try {
    // Get the form response
    var formResponse = e.response;
    var formId = e.source.getId();
    var itemResponses = formResponse.getItemResponses();
    var data = {};
    
    // Add form ID to the data
    data['form_id'] = formId;
    
    // Process each question and answer
    for (var i = 0; i < itemResponses.length; i++) {
      var item = itemResponses[i].getItem();
      var question = item.getTitle();
      var answer = itemResponses[i].getResponse();
      
      // Handle different types of responses
      if (Array.isArray(answer)) {
        // For checkbox or grid questions
        data[question] = answer.join(', ');
      } else if (typeof answer === 'object' && answer !== null) {
        // For some complex response types
        data[question] = JSON.stringify(answer);
      } else {
        // For simple text responses
        data[question] = answer;
      }
    }
    
    // Add timestamp
    data['timestamp'] = new Date().toISOString();
    
    // Prepare the payload
    var payload = JSON.stringify(data);
    
    // Set up the request options
    var options = {
      'method': 'post',
      'contentType': 'application/json',
      'payload': payload,
      'muteHttpExceptions': true
    };
    
    // Send the data to the webhook
    var response = UrlFetchApp.fetch(WEBHOOK_URL, options);
    
    // Log the response
    Logger.log('Webhook response: ' + response.getContentText());
    Logger.log('Response code: ' + response.getResponseCode());
    
    return true;
  } catch (error) {
    // Log any errors
    Logger.log('Webhook error: ' + error.toString());
    return false;
  }
}

/**
 * Test function to verify the webhook connection
 * You can run this function manually to test the connection
 */
function testWebhook() {
  var testData = {
    'test': 'This is a test submission',
    'form_id': 'test_form',
    'timestamp': new Date().toISOString()
  };
  
  var payload = JSON.stringify(testData);
  
  var options = {
    'method': 'post',
    'contentType': 'application/json',
    'payload': payload,
    'muteHttpExceptions': true
  };
  
  try {
    var response = UrlFetchApp.fetch(WEBHOOK_URL, options);
    Logger.log('Test webhook response: ' + response.getContentText());
    Logger.log('Response code: ' + response.getResponseCode());
  } catch (error) {
    Logger.log('Test webhook error: ' + error.toString());
  }
}

/**
 * Sets up the trigger to run onSubmit when a form is submitted
 * You only need to run this once to set up the trigger
 */
function createFormSubmitTrigger() {
  var form = FormApp.getActiveForm();
  ScriptApp.newTrigger('onSubmit')
    .forForm(form)
    .onFormSubmit()
    .create();
  Logger.log('Form submit trigger created for form: ' + form.getTitle());
}

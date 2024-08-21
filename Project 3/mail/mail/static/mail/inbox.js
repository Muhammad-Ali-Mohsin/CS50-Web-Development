document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Send email button
  document.querySelector('#send-email').addEventListener('click', send_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#compose-error').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-title').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Delete existing emails
  document.querySelector('#emails-list').innerHTML = '<br>';

  // Retrieve emails for mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {

      // Creates a list item for each email and adds it to the list
      emails.forEach(email => {
        
        // Create the HTML elements for the email content
        let sender = document.createElement('h6');
        sender.innerHTML = email['sender'];
        let subject = document.createElement('h6');
        subject.innerHTML = email['subject'];
        let timespan = document.createElement('span');
        timespan.innerHTML = email['timestamp'];

        // Create the list item for the email and determine its background color
        let li = document.createElement('li');
        li.className = "list-group-item justify-content-between d-flex align-items-center email-item";
        if (email['read'] === true) {
          li.style.backgroundColor = '#DDDDDD';
        }

        // Adds the email content to the list item
        li.append(sender);
        li.append(subject);
        li.append(timespan);

        // Adds an event listener to the email and adds to email list
        li.addEventListener('click', () => load_email(email['id'], mailbox));
        document.querySelector('#emails-list').append(li);
      });
  });
}

function reply_email(email_id) {
  compose_email();
  fetch (`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {

    // Fill fields
    document.querySelector('#compose-recipients').value = email['sender'];
    let subject = document.querySelector('#compose-subject');
    if (email['subject'].substring(0, 3) === "RE: "){
      subject.value = email['subject'];
    } else {
      subject.value = "RE: " + email['subject'];
    }
    document.querySelector('#compose-body').value = "On " + email['timestamp'] + " " + email['sender'] + " wrote:\n" + email['body'];
  })
}

function load_email(email_id, mailbox) {

  // Show the email and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {

    // Display email
    document.querySelector('#email-subject').innerHTML = `Subject: ${email["subject"]}`;
    document.querySelector('#email-sender').innerHTML = `Sent by: ${email["sender"]}`;
    document.querySelector('#email-recipients').innerHTML = `Recipient(s): ${email["recipients"]}`;
    document.querySelector('#email-timestamp').innerHTML = `Recieved: ${email["timestamp"]}`;
    document.querySelector('#email-body').innerHTML = `${email["body"]}`;

    // Add archive button
    let archiveButton = document.querySelector('#btn-archive');
    let replyButton = document.querySelector('#btn-reply');
    if (mailbox === "sent") {
      archiveButton.style.display = 'none';
      replyButton.style.display = 'none';
    } else {
      archiveButton.style.display = 'block';
      archiveButton.innerHTML = email['archived'] ? 'Unarchive Email' : 'Archive Email';
      archiveButton.onclick = () => {

        // Archives/Unarchives the email
        fetch(`/emails/${email_id}`, {
          method: 'PUT',
          body: JSON.stringify({
              archived: !email['archived']
          })
        })
        .then(() => load_mailbox('inbox'))
      };

      replyButton.style.display = 'block';
      replyButton.onclick = () => reply_email(email_id);

    }

    // Mark the email as read
    fetch(`/emails/${email_id}`, {
      method: 'PUT',
      body: JSON.stringify({
          read: true
      })
    })
  });
}

function send_email() {

  // Retrieves form data
  let recipients = document.querySelector('#compose-recipients').value;
  let subject = document.querySelector('#compose-subject').value;
  let body = document.querySelector('#compose-body').value;

  // Submit post request to send email
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json())
  .then(result => {

      // If request was unsuccessful, show error message
      if (result["error"]) {
        document.querySelector('#compose-error').style.display = 'block';
        document.querySelector('#compose-error').innerHTML = result["error"];
      } else{

        // Redirect to sent mailbox
        load_mailbox('sent')
      }
  });

  // Prevent page from refreshing
  event.preventDefault();

}
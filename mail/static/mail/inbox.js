document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click',() => compose_email());
  document.querySelector('#compose-form').addEventListener('submit', () => send_mail(event));

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(email) {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-content').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  if (email === undefined) {
    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';

  } else {
    console.log(email);
    document.querySelector('#compose-recipients').value = email.sender;

    if (email.subject.substring(0,4)==='Re: ') {
      document.querySelector('#compose-subject').value = email.subject;
    } else {
      document.querySelector('#compose-subject').value = 'Re: '+ email.subject;
    }
    document.querySelector('#compose-body').value = `\n\nOn ${email.timestamp}, ${email.sender} wrote:\n${email.body}`;


  }

}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-content').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3 class="title">${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  //GET Request to fetch emails
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
  //     // Print emails
      console.log(emails);

      //loop to create an element for each email
      emails.forEach(email => {
        const container = document.createElement('div');
        container.setAttribute('id', 'container_mail')

        //change color if email is read
        if (email.read === true) {
          container.style.backgroundColor = '#e2e2ff';
        } else {
          container.style.backgroundColor = 'white';
        }

        container.innerHTML = `
        <div class="d-flex flex-row bd-highlight">
          <div id="mail_list_title" class="d-inline p-2 bd-highlight">${email.subject}</div>
        </div>
        <div class="d-flex flex-row bd-highlight">
          <div id="mail_list_info" class="d-inline p-2 bd-highlight">From: ${email.sender}</div>
          <div id="mail_list_info" class="d-inline p-2 bd-highlight">${email.timestamp}</div>
        </div>`;

        container.addEventListener('click', () => clickEmail(email.id));
      
        document.querySelector('#emails-view').append(container);

      });
      
      document.querySelector('#emails-view').append(document.createElement('hr'));
  
  });

}

//function to send email
function send_mail(event) {
  event.preventDefault();

  //save mail content to variables
  const mail_body = String(event.target.querySelector('#compose-body').value);
  const mail_subject = String(event.target.querySelector('#compose-subject').value);
  const mail_recipients = String(event.target.querySelector('#compose-recipients').value);
  

  //POST method to send the email trough the API
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: mail_recipients,
      subject: mail_subject,
      body: mail_body
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      if (result.error ===undefined ) {
        load_mailbox('inbox');
      } else {
        alert(result.error) ;  
      }
  });
}

function clickEmail(email_id) {

   // Show the email-content and hide other views
   document.querySelector('#emails-view').style.display = 'none';
   document.querySelector('#compose-view').style.display = 'none';
   document.querySelector('#email-content').style.display = 'block';

  //GET email content
  fetch(`emails/${email_id}`)
  .then(response => response.json())
  .then(email => {

    if (email.error === undefined) {
      

      // Mark email as read with PUT request
      if (email.read === false) {
        console.log("email was read now");
        change_state(email, 'read');
      }

      //add an element for the email contents
      const element = document.createElement('div');
      element.setAttribute('class', 'email_content');

      element.innerHTML = (`
        From: ${email.sender} <br/>
        To: ${email.recipients} <br/>
        Time: ${email.timestamp} <br/>
        <h2>${email.subject}</h2>
        <textarea readonly class="form-control">${email.body}</textarea>`);
    
      document.querySelector('#email-content').innerHTML = element.innerHTML;

      var reply_btn = document.createElement('BUTTON');
      reply_btn.setAttribute('class', 'btn btn-primary btn_mail');
      reply_btn.innerHTML = 'Reply';
      reply_btn.addEventListener('click', () => compose_email(email));

      document.querySelector('#email-content').append(reply_btn);

      //archive / unarchive button if email is not sent
      if (email.sender != email.user) {
        var button_value = (email.archived) ? 'Unarchive this email.' : 'Archive this email.'

        var archive_btn = document.createElement('BUTTON');
        archive_btn.setAttribute('class', 'btn btn-primary btn_mail');
        archive_btn.innerHTML = button_value;
        archive_btn.addEventListener('click', () => change_state(email, 'archive'));

        document.querySelector('#email-content').append(archive_btn);
      }
    } else {
      alert(email.error);
    }


  });
}

function change_state(email_object, state) {
  var new_read = email_object.read;
  var new_archived = email_object.archived;
  
  //if state is read, change the read state
  // if state is archived, change archive state
  
  new_read = (state === 'read') ? !new_read : new_read;
  new_archived = (state === 'archive') ? !new_archived : new_archived;

  fetch(`emails/${email_object.id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: new_read,
        archived: new_archived
    })
  })
  .then(() => {
    clickEmail(email_object.id);
  })
  .then(() => {
    if (state==='archive') {
      load_mailbox('inbox');
    }
  });
}
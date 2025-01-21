


// Function to add a message to the chatbox
// function addMessage(sender, message) {
//     const chatBox = document.querySelector('.chat-box');
//     const messageBlock = document.createElement('div');
//     messageBlock.classList.add('message-block', sender);

//     const messageText = document.createElement('div');
//     messageText.classList.add('message');
//     messageText.textContent = message;

//     messageBlock.appendChild(messageText);
//     chatBox.appendChild(messageBlock);

//     // Scroll to the bottom of the chatbox for new messages
//     chatBox.scrollTop = chatBox.scrollHeight;
// }




// Function to add a message to the chatbox
function addMessage(sender, message) {
    const chatBox = document.querySelector('.chat-box');
    const messageBlock = document.createElement('div');
    messageBlock.classList.add('message-block', sender);

    const messageText = document.createElement('div');
    messageText.classList.add('message');

    // Check if the message contains a link
    if (message.includes('http')) {
        const parts = message.split('\n\n');
        messageText.innerHTML = `${parts[0]}<br><a href="${parts[1].match(/https?:\/\/\S+/)[0]}" target="_blank">Document Link</a>`;
    } else {
        messageText.textContent = message;
    }

    messageBlock.appendChild(messageText);
    chatBox.appendChild(messageBlock);

    // Scroll to the bottom of the chatbox for new messages
    chatBox.scrollTop = chatBox.scrollHeight;
}


// Function to select a module and proceed to the next step
function selectModule() {
    const module = document.getElementById('selected_module').value;
    if (!module) {
        alert('Please select a module');
        return;
    }

    addMessage('user', `Selected Module: ${module}`);
    addMessage('bot', 'Please select an area.');

    const form = document.getElementById('module-form');
    form.innerHTML = ''; // Clear previous inputs
    const input = document.createElement('input');
    input.type = 'hidden';
    input.name = 'module';
    input.value = module;
    form.appendChild(input);
    form.submit();
}

// Function to select an area and proceed to the next step
function selectArea() {
    const module = document.getElementById('area-form-module').value;
    const area = document.getElementById('selected_area').value;
    if (!area) {
        alert('Please select an area');
        return;
    }

    addMessage('user', `Selected Area: ${area}`);
    addMessage('bot', 'Please select a question.');

    const form = document.getElementById('area-form');
    form.innerHTML = ''; // Clear previous inputs
    const moduleInput = document.createElement('input');
    moduleInput.type = 'hidden';
    moduleInput.name = 'module';
    moduleInput.value = module;
    form.appendChild(moduleInput);

    const areaInput = document.createElement('input');
    areaInput.type = 'hidden';
    areaInput.name = 'area';
    areaInput.value = area;
    form.appendChild(areaInput);

    form.submit();
}

// Function to select a question and proceed to the next step
function selectQuestion() {
    const module = document.getElementById('question-form-module').value;
    const area = document.getElementById('question-form-area').value;
    const question = document.getElementById('selected_question').value;
    if (!question) {
        alert('Please select a question');
        return;
    }

    addMessage('user', `Selected Question: ${question}`);
    addMessage('bot', 'Thank you for your selection. Processing your request...');

    const form = document.getElementById('question-form');
    form.innerHTML = ''; // Clear previous inputs
    const moduleInput = document.createElement('input');
    moduleInput.type = 'hidden';
    moduleInput.name = 'module';
    moduleInput.value = module;
    form.appendChild(moduleInput);

    const areaInput = document.createElement('input');
    areaInput.type = 'hidden';
    areaInput.name = 'area';
    areaInput.value = area;
    form.appendChild(areaInput);

    const questionInput = document.createElement('input');
    questionInput.type = 'hidden';
    questionInput.name = 'question';
    questionInput.value = question;
    form.appendChild(questionInput);

    form.submit();
}




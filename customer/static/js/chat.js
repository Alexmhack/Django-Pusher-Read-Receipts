(function() {
    'use strict';

    var csrftoken = Cookies.get('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    var pusher = new Pusher('399efdfd937640a8af99', {
        authEndpoint: '/pusher/auth/',
        auth: {
            headers: {
              'X-CSRFToken': csrftoken
            }
        },
        cluster: 'ap2',
        encrypted: true
    });

    // ----------------------------------------------------
    // Chat Details
    // ----------------------------------------------------

    let chat = {
        name: undefined,
        email: undefined,
        myChannel: undefined,
    }


    // ----------------------------------------------------
    // Targeted Elements
    // ----------------------------------------------------

    const chatPage = $(document)
    const chatWindow = $('.chatbubble')
    const chatHeader = chatWindow.find('.unexpanded')
    const chatBody = chatWindow.find('.chat-window')


    // ----------------------------------------------------
    // Register helpers
    // ----------------------------------------------------

    let helpers = {

        // ----------------------------------------------------
        // Toggles the display of the chat window.
        // ----------------------------------------------------

        ToggleChatWindow: function() {
            chatWindow.toggleClass('opened')
            chatHeader.find('.title').text(
                chatWindow.hasClass('opened') ? 'Minimize Chat Window' : 'Chat with Support'
            )
        },

        // --------------------------------------------------------------------
        // Show the appropriate display screen. Login screen or Chat screen.
        // --------------------------------------------------------------------

        ShowAppropriateChatDisplay: function() {
            (chat.name) ? helpers.ShowChatRoomDisplay(): helpers.ShowChatInitiationDisplay()
        },

        // ----------------------------------------------------
        // Show the enter details form.
        // ----------------------------------------------------

        ShowChatInitiationDisplay: function() {
            chatBody.find('.chats').removeClass('active')
            chatBody.find('.login-screen').addClass('active')
        },

        // ----------------------------------------------------
        // Show the chat room messages display.
        // ----------------------------------------------------

        ShowChatRoomDisplay: function() {
            chatBody.find('.chats').addClass('active')
            chatBody.find('.login-screen').removeClass('active')

            setTimeout(function() {
                chatBody.find('.loader-wrapper').hide()
                chatBody.find('.input, .messages').show()
            }, 2000)
        },

        // ----------------------------------------------------
        // Append a message to the chat messages UI.
        // ----------------------------------------------------

        NewChatMessage: function(message) {
            if (message !== undefined) {
                const messageClass = message.sender !== chat.email ? 'support' : 'user'

                chatBody.find('ul.messages').append(
                    `<li class="clearfix message ${messageClass}">
                            <div class="sender">${message.name}</div>
                            <div class="message">${message.text}</div>
                        </li>`
                )


                chatBody.scrollTop(chatBody[0].scrollHeight)
            }
        },

        // ----------------------------------------------------
        // Send a message to the chat channel.
        // ----------------------------------------------------

        SendMessageToSupport: function(evt) {

            evt.preventDefault()

            let createdAt = new Date()
            createdAt = createdAt.toLocaleString()

            const message = $('#newMessage').val().trim()

            chat.myChannel.trigger('client-guest-new-message', {
                'sender': chat.name,
                'email': chat.email,
                'text': message,
                'createdAt': createdAt
            });

            helpers.NewChatMessage({
                'text': message,
                'name': chat.name,
                'sender': chat.email
            })

            console.log("Message added!")

            $('#newMessage').val('')
        },

        // ----------------------------------------------------
        // Logs user into a chat session.
        // ----------------------------------------------------

        LogIntoChatSession: function(evt) {
            const name = $('#fullname').val().trim()
            const email = $('#email').val().trim().toLowerCase()

            axios.defaults.xsrfHeaderName = "X-CSRFToken";

            // Disable the form
            chatBody.find('#loginScreenForm input, #loginScreenForm button').attr('disabled', true)

            if ((name !== '' && name.length >= 3) && (email !== '' && email.length >= 5)) {
                $.ajax({
                    methods: 'post',
                    url: '/new/guest/',
                    data: { name, email },
                    success: function(data) {
                        console.log(data);
                        chat.name = data.name
                        chat.email = data.email
                        chat.myChannel = pusher.subscribe('private-' + data.email);
                        helpers.ShowAppropriateChatDisplay()
                    },
                    error: function(err) {
                        console.error(err);
                    }
                })
            } else {
                alert('Enter a valid name and email.')
            }

            evt.preventDefault()
        }
    }

    // ------------------------------------------------------------------
    // Listen for a new message event from the admin
    // ------------------------------------------------------------------

    pusher.bind('client-support-new-message', function(data) {
        helpers.NewChatMessage(data)
    })


    // ----------------------------------------------------
    // Register page event listeners
    // ----------------------------------------------------

    chatPage.ready(helpers.ShowAppropriateChatDisplay)
    chatHeader.on('click', helpers.ToggleChatWindow)
    chatBody.find('#loginScreenForm').on('submit', helpers.LogIntoChatSession)
    chatBody.find('#messageSupport').on('submit', helpers.SendMessageToSupport)
}())
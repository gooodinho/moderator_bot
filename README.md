## Shortcut telegram bot created to help moderate a group
_Created for the Axelar crypto project, as part of the Quantum Community Program_

### To use the shortcut in a group, write `!SHORTCUT`
To use shortcuts in a group, you need to add the bot to the group and make it an administrator, with the right to delete messages.

### To launch a bot for your group
1. Download all files
2. Fill `.env.example` file with your data and rename it to `.env`
3. Run `docker-compose up`

### How to add new admin
To create your "add admin" deep link use `/add_admin` command. It can only be used once, after which you can create a new link.

When a user who clicks on this link and starts the bot, he will be added to the administrators.

### List of admin functions
**1. Shortcuts CRUD**

**2. Add new admins**

**3. Use shortcuts**


### Example of using shortcuts
You have created a shortcut called "hello", which should be replaced by the text _"Hello World, It's shortcut bot".

After you send a `!hello` message to the group, the bot will delete your message and send the text "_Hello World, It's shortcut bot"_.
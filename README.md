## Pew Pew
A simple shooting game project for network programming class.

Use asynchronize client-server architecture. Details are below.

### Dependency
 - Python 2.7+
 - ParticlePlay Engine (Python 2.7+ version)

### Starting server
Run `python PewPewServer.py` command on the terminal.

### Run a client
Run `python PewPewClient.py` command on the terminal and enter server IP address.

### Asynchronize Client-Server Architecture
By running and updating the game logic on server, this helps every clients display a proper and corrected data exactly from server. Server is using a master-slave architecture to help connect with each client easier.

Clients only send current player position, shoot request to server and receive a packet from server to display a game state.
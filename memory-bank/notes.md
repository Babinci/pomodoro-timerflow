# Development Notes

This file contains miscellaneous notes, conversations, and thoughts related to the development process that don't fit neatly into the other memory bank files.

## Web App Connection Longevity

I have a problem sometimes if I have the web app opened for about 2 hours and I am not active - I lose connection.

This is bad. I should not lose connection.

This should work like this:
If there is a working session/break/long break and I am not coming to the computer even for a long time, I should be able to use it normally - so state should be saved.

Potential solution: Store states as checkpoints in the database. See checkpoint_states.md for the implementation details.

## Timer Problems

Current status: Implemented changes, now testing.

## Task Debugging Notes

When debugging issues, consider:
1. Check browser console for errors
2. Verify WebSocket connections are maintained
3. Test with different browsers to isolate browser-specific issues
4. Check for race conditions in state updates
5. Verify that database transactions are completing properly

## Development Workflow Notes

- Wear OS development is being done in Android Studio on Windows with git syncs between the Linux PC
- Docker server can be restarted with the `./restart_docker.sh` command
- Database migrations work with Docker restarting
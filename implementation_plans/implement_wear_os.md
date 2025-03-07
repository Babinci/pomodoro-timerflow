# Pomodoro TimerFlow Wear OS App Setup Guide

This guide will walk you through setting up and running the Pomodoro TimerFlow Wear OS app.

## Prerequisites

Before getting started, ensure you have the following installed:

- Node.js (LTS version recommended)
- NPM or Yarn
- Java Development Kit (JDK) 11 or newer
- Android Studio (latest version)
- Wear OS emulator or physical Wear OS device
- VS Code with recommended extensions:
  - React Native Tools
  - ES7+ React/Redux/React-Native snippets
  - ESLint
  - Prettier

## Step 2: Create the Wear OS App Directory

```bash
mkdir -p frontend-apps/wear-app
cd frontend-apps/wear-app
```

status: done


## Step 3: Initialize the React Native Project

```bash
npx @react-native-community/cli@latest init PomodoroWear

cd PomodoroWear
```
status: done
## Step 4: Install Dependencies

```bash
npm install react-native-wear-os   - error: npm error 404 Not Found - GET https://registry.npmjs.org/react-native-wear-os - Not found  <--- irrelevant- we are ommiting this
npm install react-native-wear-connectivity- success: added 1 package, and audited 931 packages in 3s
npm install @react-navigation/native- success:  added 12 packages, and audited 943 packages in 3s
npm install @react-navigation/material-top-tabs- success:  added 9 packages, and audited 952 packages in 6s
npm install react-native-tab-view- success: up to date, audited 952 packages in 3s
npm install react-native-reanimated- success: added 2 packages, and audited 954 packages in 4s
npm install react-native-gesture-handler- success:  added 5 packages, and audited 959 packages in 4s
npm install react-native-screens- success:  added 3 packages, and audited 962 packages in 3s
npm install react-native-safe-area-context- success: up to date, audited 962 packages in 3s
npm install @react-native-async-storage/async-storage success: added 3 packages, and audited 965 packages in 3s
```
status: done, ommiting 
## Step 5: Create Project Structure

Create the following directory structure:

```
src/
├── components/
├── config/
├── context/
├── hooks/
├── screens/
│   ├── LoginScreen.js
│   ├── TimerScreen.js
│   ├── ControlsScreen.js
│   └── TaskDescriptionScreen.js
└── services/
    └── wearConnectivity.js   <--- i have this file blank
```
status 
## Step 6: Configure Android for Wear OS

1. Update the `android/app/build.gradle` file with the Wear OS configurations as provided in the setup code.
2. Update the `android/app/src/main/AndroidManifest.xml` file to include Wear OS features and permissions.

## Step 7: Configure Project Files

Copy the provided code files to their respective locations in the project structure.

## Step 8: Setup Android Studio for Wear OS

1. Open Android Studio
2. Go to AVD Manager (Android Virtual Device Manager)
3. Create a new virtual device
4. Select "Wear OS" category
5. Choose a Wear OS device (e.g., Wear OS Large Round)
6. Select a system image (API level 30 or higher recommended)
7. Finish the setup and name your emulator

## Step 9: Running the App

### Using VS Code:

1. Open the PomodoroWear project in VS Code
2. Start the Metro bundler:
   ```bash
   npx react-native start
   ```
3. In a new terminal window, run:
   ```bash
   npx react-native run-android
   ```

### Using Android Studio:

1. Open the `android` folder in Android Studio
2. Select your Wear OS emulator from the device dropdown
3. Click the Run button

## Troubleshooting

### Connection to Backend
- Ensure your backend server is running
- Check the `apiConfig.js` file to ensure the correct IP and port are set

### Wear OS Emulator Issues
- If the emulator seems slow, consider increasing RAM allocation in AVD settings
- For physical devices, ensure Developer Options and USB debugging are enabled

### Common Build Errors
- If you encounter build errors related to SDK versions, check your `build.gradle` files
- Ensure your `ANDROID_HOME` environment variable is set correctly

## Next Steps

Once your app is running successfully, you can:

1. Test the login functionality
2. Verify the timer sync between your backend and the Wear OS app
3. Test vibration notifications when work sessions end
4. Customize the UI to match your branding

## Documentation and Resources

For additional help, refer to:
- [React Native documentation](https://reactnative.dev/docs/getting-started)
- [Wear OS developer documentation](https://developer.android.com/training/wearables)
- [React Native Wear Connectivity documentation](https://github.com/mthuong/react-native-wear-connectivity)
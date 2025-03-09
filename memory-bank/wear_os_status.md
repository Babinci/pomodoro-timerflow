# Wear OS App Status

## Completed Steps

- Created the Wear OS app directory.
- Initialized the React Native project.
- Installed dependencies (excluding `react-native-wear-os`).
- Created the project structure.
- Configured Android for Wear OS.
- Invented project files in `frontend-apps/wear-app/PomodoroWear/src`.
- Installed React Native Tools and Android iOS Emulator extensions in VS Code.
- Installed Java on Linux.
- Installed Android Studio on Windows Machine i am developing from

## Current Challenges

- making build of wear os app to launch in android studio



build success!!
wojtek@wojtek-Latitude-E6420:~/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/android$ ./gradlew assembleDebug

> Configure project :react-native-reanimated
Android gradle plugin: 8.8.0
Gradle: 8.12

> Task :app:createBundleWearDebugJsAndAssets
 WARN  the transform cache was reset.
                Welcome to Metro v0.81.3
              Fast - Scalable - Integrated


Writing bundle output to: /home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/android/app/build/generated/assets/createBundleWearDebugJsAndAssets/index.android.bundle
Writing sourcemap output to: /home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/android/app/build/intermediates/sourcemaps/react/wearDebug/index.android.bundle.packager.map
Done writing bundle output
Done writing sourcemap output
Copying 19 asset files
Done copying assets
/home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/android/app/build/generated/assets/createBundleWearDebugJsAndAssets/index.android.bundle:1265:23: warning: the variable "DebuggerInternal" was not declared in function "__shouldPauseOnThrow"
        return typeof DebuggerInternal !== 'undefined' && DebuggerInternal.sh...
                      ^~~~~~~~~~~~~~~~
/home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/android/app/build/generated/assets/createBundleWearDebugJsAndAssets/index.android.bundle:6135:7: warning: the variable "setTimeout" was not declared in function "logUncaughtError"
      setTimeout(function () {
      ^~~~~~~~~~
/home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/android/app/build/generated/assets/createBundleWearDebugJsAndAssets/index.android.bundle:6110:49: warning: the variable "reportError" was not declared in anonymous function " 144#"
...alError = "function" === typeof reportError ? reportError : function (erro...
                                   ^~~~~~~~~~~
/home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/android/app/build/generated/assets/createBundleWearDebugJsAndAssets/index.android.bundle:6926:53: warning: the variable "AbortController" was not declared in anonymous function " 144#"
...ocal = "undefined" !== typeof AbortController ? AbortController : function...
                                 ^~~~~~~~~~~~~~~
/home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/android/app/build/generated/assets/createBundleWearDebugJsAndAssets/index.android.bundle:8917:31: warning: the variable "nativeFabricUIManager" was not declared in anonymous function " 144#"
  var _nativeFabricUIManage = nativeFabricUIManager,
                              ^~~~~~~~~~~~~~~~~~~~~
/home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/android/app/build/generated/assets/createBundleWearDebugJsAndAssets/index.android.bundle:8967:21: warning: the variable "clearTimeout" was not declared in anonymous function " 144#"
    cancelTimeout = clearTimeout;
                    ^~~~~~~~~~~~
/home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/android/app/build/generated/assets/createBundleWearDebugJsAndAssets/index.android.bundle:8988:49: warning: the variable "RN$enableMicrotasksInReact" was not declared in anonymous function " 144#"
... "undefined" !== typeof RN$enableMicrotasksInReact && !!RN$enableMicrotask...
                           ^~~~~~~~~~~~~~~~~~~~~~~~~~
/home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/android/app/build/generated/assets/createBundleWearDebugJsAndAssets/index.android.bundle:8989:47: warning: the variable "queueMicrotask" was not declared in anonymous function " 144#"
...otask = "function" === typeof queueMicrotask ? queueMicrotask : scheduleTi...
                                 ^~~~~~~~~~~~~~
/home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/android/app/build/generated/assets/createBundleWearDebugJsAndAssets/index.android.bundle:9042:30: warning: the variable "__REACT_DEVTOOLS_GLOBAL_HOOK__" was not declared in anonymous function " 144#"
  if ("undefined" !== typeof __REACT_DEVTOOLS_GLOBAL_HOOK__) {
                             ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
/home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/android/app/build/generated/assets/createBundleWearDebugJsAndAssets/index.android.bundle:11010:5: warning: the variable "setImmediate" was not declared in function "handleResolved"
    setImmediate(function () {
    ^~~~~~~~~~~~
/home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/android/app/build/generated/assets/createBundleWearDebugJsAndAssets/index.android.bundle:14755:12: warning: the variable "fetch" was not declared in anonymous function " 410#"
    fetch: fetch,
           ^~~~~
/home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/android/app/build/generated/assets/createBundleWearDebugJsAndAssets/index.android.bundle:14756:14: warning: the variable "Headers" was not declared in anonymous function " 410#"
    Headers: Headers,
             ^~~~~~~
/home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/android/app/build/generated/assets/createBundleWearDebugJsAndAssets/index.android.bundle:14757:14: warning: the variable "Request" was not declared in anonymous function " 410#"
    Request: Request,
             ^~~~~~~
/home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/android/app/build/generated/assets/createBundleWearDebugJsAndAssets/index.android.bundle:14758:15: warning: the variable "Response" was not declared in anonymous function " 410#"
    Response: Response
              ^~~~~~~~
/home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/android/app/build/generated/assets/createBundleWearDebugJsAndAssets/index.android.bundle:14915:24: warning: the variable "FileReader" was not declared in function "readBlobAsArrayBuffer"
      var reader = new FileReader();
                       ^~~~~~~~~~
/home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/android/app/build/generated/assets/createBundleWearDebugJsAndAssets/index.android.bundle:14966:36: warning: the variable "Blob" was not declared in anonymous function " 421#"
        } else if (support.blob && Blob.prototype.isPrototypeOf(body)) {
                                   ^~~~
/home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/android/app/build/generated/assets/createBundleWearDebugJsAndAssets/index.android.bundle:14968:40: warning: the variable "FormData" was not declared in anonymous function " 421#"
        } else if (support.formData && FormData.prototype.isPrototypeOf(body)) {
                                       ^~~~~~~~
/home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/android/app/build/generated/assets/createBundleWearDebugJsAndAssets/index.android.bundle:14970:44: warning: the variable "URLSearchParams" was not declared in anonymous function " 421#"
...e if (support.searchParams && URLSearchParams.prototype.isPrototypeOf(body...
                                 ^~~~~~~~~~~~~~~
/home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/android/app/build/generated/assets/createBundleWearDebugJsAndAssets/index.android.bundle:15223:23: warning: the variable "XMLHttpRequest" was not declared in anonymous function " 431#"
        var xhr = new XMLHttpRequest();
                      ^~~~~~~~~~~~~~
/home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/android/app/build/generated/assets/createBundleWearDebugJsAndAssets/index.android.bundle:14768:71: warning: the variable "self" was not declared in anonymous function " 413#"
...undefined' && globalThis || typeof self !== 'undefined' && self ||
                                      ^~~~
/home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/android/app/build/generated/assets/createBundleWearDebugJsAndAssets/index.android.bundle:22816:37: warning: the variable "MessageChannel" was not declared in anonymous function " 719#"
  };else if ("undefined" !== typeof MessageChannel) {
                                    ^~~~~~~~~~~~~~
/home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/android/app/build/generated/assets/createBundleWearDebugJsAndAssets/index.android.bundle:22831:62: warning: the variable "nativeRuntimeScheduler" was not declared in anonymous function " 719#"
... = "undefined" !== typeof nativeRuntimeScheduler ? nativeRuntimeScheduler....
                             ^~~~~~~~~~~~~~~~~~~~~~
/home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/android/app/build/generated/assets/createBundleWearDebugJsAndAssets/index.android.bundle:59569:9: warning: the variable "REACT_NAVIGATION_DEVTOOLS" was not declared in anonymous function " 2089#"
        REACT_NAVIGATION_DEVTOOLS.set(refContainer.current, {
        ^~~~~~~~~~~~~~~~~~~~~~~~~
/home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/android/app/build/generated/assets/createBundleWearDebugJsAndAssets/index.android.bundle:62846:26: warning: the variable "ResizeObserver" was not declared in anonymous function " 2205#"
      var observer = new ResizeObserver(function (entries) {
                         ^~~~~~~~~~~~~~

> Task :react-native-safe-area-context:processDebugManifest
package="com.th3rdwave.safeareacontext" found in source AndroidManifest.xml: /home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/node_modules/react-native-safe-area-context/android/src/main/AndroidManifest.xml.
Setting the namespace via the package attribute in the source AndroidManifest.xml is no longer supported, and the value is ignored.
Recommendation: remove package="com.th3rdwave.safeareacontext" from the source AndroidManifest.xml: /home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/node_modules/react-native-safe-area-context/android/src/main/AndroidManifest.xml.

> Task :react-native-async-storage_async-storage:processDebugManifest
package="com.reactnativecommunity.asyncstorage" found in source AndroidManifest.xml: /home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/node_modules/@react-native-async-storage/async-storage/android/src/main/AndroidManifest.xml.
Setting the namespace via the package attribute in the source AndroidManifest.xml is no longer supported, and the value is ignored.
Recommendation: remove package="com.reactnativecommunity.asyncstorage" from the source AndroidManifest.xml: /home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/node_modules/@react-native-async-storage/async-storage/android/src/main/AndroidManifest.xml.

> Task :react-native-async-storage_async-storage:compileDebugJavaWithJavac
Note: Some input files use or override a deprecated API.
Note: Recompile with -Xlint:deprecation for details.
Note: /home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/node_modules/@react-native-async-storage/async-storage/android/src/javaPackage/java/com/reactnativecommunity/asyncstorage/AsyncStoragePackage.java uses unchecked or unsafe operations.
Note: Recompile with -Xlint:unchecked for details.

> Task :react-native-reanimated:compileDebugJavaWithJavac
Note: Some input files use or override a deprecated API.
Note: Recompile with -Xlint:deprecation for details.
Note: Some input files use unchecked or unsafe operations.
Note: Recompile with -Xlint:unchecked for details.

> Task :react-native-wear-connectivity:compileDebugJavaWithJavac
Note: Some input files use or override a deprecated API.
Note: Recompile with -Xlint:deprecation for details.

> Task :react-native-safe-area-context:compileDebugKotlin
w: file:///home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/node_modules/react-native-safe-area-context/android/src/main/java/com/th3rdwave/safeareacontext/SafeAreaView.kt:59:23 'val uiImplementation: UIImplementation!' is deprecated. Deprecated in Java.
w: file:///home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/node_modules/react-native-safe-area-context/android/src/paper/java/com/th3rdwave/safeareacontext/InsetsChangeEvent.kt:19:16 This declaration overrides a deprecated member but is not marked as deprecated itself. Please add the '@Deprecated' annotation or suppress the diagnostic.

> Task :react-native-screens:compileDebugKotlin
w: file:///home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/node_modules/react-native-screens/android/src/main/java/com/swmansion/rnscreens/CustomToolbar.kt:19:33 'class FrameCallback : Choreographer.FrameCallback' is deprecated. Use Choreographer.FrameCallback instead.
w: file:///home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/node_modules/react-native-screens/android/src/main/java/com/swmansion/rnscreens/CustomToolbar.kt:20:18 'class FrameCallback : Choreographer.FrameCallback' is deprecated. Use Choreographer.FrameCallback instead.
w: file:///home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/node_modules/react-native-screens/android/src/main/java/com/swmansion/rnscreens/RNScreensPackage.kt:66:17 'constructor(name: String, className: String, canOverrideExistingModule: Boolean, needsEagerInit: Boolean, hasConstants: Boolean, isCxxModule: Boolean, isTurboModule: Boolean): ReactModuleInfo' is deprecated. This constructor is deprecated and will be removed in the future. Use ReactModuleInfo(String, String, boolean, boolean, boolean, boolean)].
w: file:///home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/node_modules/react-native-screens/android/src/main/java/com/swmansion/rnscreens/Screen.kt:47:77 Unchecked cast of '(androidx.coordinatorlayout.widget.CoordinatorLayout.Behavior<android.view.View!>?..androidx.coordinatorlayout.widget.CoordinatorLayout.Behavior<*>?)' to 'com.google.android.material.bottomsheet.BottomSheetBehavior<com.swmansion.rnscreens.Screen>'.
w: file:///home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/node_modules/react-native-screens/android/src/main/java/com/swmansion/rnscreens/ScreenContainer.kt:33:33 'class FrameCallback : Choreographer.FrameCallback' is deprecated. Use Choreographer.FrameCallback instead.
w: file:///home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/node_modules/react-native-screens/android/src/main/java/com/swmansion/rnscreens/ScreenContainer.kt:34:18 'class FrameCallback : Choreographer.FrameCallback' is deprecated. Use Choreographer.FrameCallback instead.
w: file:///home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/node_modules/react-native-screens/android/src/main/java/com/swmansion/rnscreens/ScreenStackFragment.kt:281:31 'var targetElevation: Float' is deprecated. Deprecated in Java.
w: file:///home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/node_modules/react-native-screens/android/src/main/java/com/swmansion/rnscreens/ScreenStackFragment.kt:284:13 'fun setHasOptionsMenu(p0: Boolean): Unit' is deprecated. Deprecated in Java.
w: file:///home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/node_modules/react-native-screens/android/src/main/java/com/swmansion/rnscreens/ScreenStackFragment.kt:642:18 This declaration overrides a deprecated member but is not marked as deprecated itself. Please add the '@Deprecated' annotation or suppress the diagnostic.
w: file:///home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/node_modules/react-native-screens/android/src/main/java/com/swmansion/rnscreens/ScreenStackFragment.kt:649:22 'fun onPrepareOptionsMenu(p0: Menu): Unit' is deprecated. Deprecated in Java.
w: file:///home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/node_modules/react-native-screens/android/src/main/java/com/swmansion/rnscreens/ScreenStackFragment.kt:652:18 This declaration overrides a deprecated member but is not marked as deprecated itself. Please add the '@Deprecated' annotation or suppress the diagnostic.
w: file:///home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/node_modules/react-native-screens/android/src/main/java/com/swmansion/rnscreens/ScreenStackFragment.kt:657:22 'fun onCreateOptionsMenu(p0: Menu, p1: MenuInflater): Unit' is deprecated. Deprecated in Java.
w: file:///home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/node_modules/react-native-screens/android/src/main/java/com/swmansion/rnscreens/ScreenStackHeaderConfig.kt:100:38 'val systemWindowInsetTop: Int' is deprecated. Deprecated in Java.
w: file:///home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/node_modules/react-native-screens/android/src/main/java/com/swmansion/rnscreens/ScreenStackHeaderConfigViewManager.kt:7:8 'class MapBuilder : Any' is deprecated. Deprecated in Java.
w: file:///home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/node_modules/react-native-screens/android/src/main/java/com/swmansion/rnscreens/ScreenStackHeaderConfigViewManager.kt:210:9 'class MapBuilder : Any' is deprecated. Deprecated in Java.
w: file:///home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/node_modules/react-native-screens/android/src/main/java/com/swmansion/rnscreens/ScreenStackHeaderConfigViewManager.kt:212:13 'class MapBuilder : Any' is deprecated. Deprecated in Java.
w: file:///home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/node_modules/react-native-screens/android/src/main/java/com/swmansion/rnscreens/ScreenStackHeaderConfigViewManager.kt:214:13 'class MapBuilder : Any' is deprecated. Deprecated in Java.
w: file:///home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/node_modules/react-native-screens/android/src/main/java/com/swmansion/rnscreens/ScreenViewManager.kt:7:8 'class MapBuilder : Any' is deprecated. Deprecated in Java.
w: file:///home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/node_modules/react-native-screens/android/src/main/java/com/swmansion/rnscreens/ScreenViewManager.kt:382:48 'class MapBuilder : Any' is deprecated. Deprecated in Java.
w: file:///home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/node_modules/react-native-screens/android/src/main/java/com/swmansion/rnscreens/ScreenViewManager.kt:383:49 'class MapBuilder : Any' is deprecated. Deprecated in Java.
w: file:///home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/node_modules/react-native-screens/android/src/main/java/com/swmansion/rnscreens/ScreenViewManager.kt:384:45 'class MapBuilder : Any' is deprecated. Deprecated in Java.
w: file:///home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/node_modules/react-native-screens/android/src/main/java/com/swmansion/rnscreens/ScreenViewManager.kt:385:52 'class MapBuilder : Any' is deprecated. Deprecated in Java.
w: file:///home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/node_modules/react-native-screens/android/src/main/java/com/swmansion/rnscreens/ScreenViewManager.kt:386:48 'class MapBuilder : Any' is deprecated. Deprecated in Java.
w: file:///home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/node_modules/react-native-screens/android/src/main/java/com/swmansion/rnscreens/ScreenViewManager.kt:387:51 'class MapBuilder : Any' is deprecated. Deprecated in Java.
w: file:///home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/node_modules/react-native-screens/android/src/main/java/com/swmansion/rnscreens/ScreenViewManager.kt:388:56 'class MapBuilder : Any' is deprecated. Deprecated in Java.
w: file:///home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/node_modules/react-native-screens/android/src/main/java/com/swmansion/rnscreens/ScreenViewManager.kt:389:57 'class MapBuilder : Any' is deprecated. Deprecated in Java.
w: file:///home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/node_modules/react-native-screens/android/src/main/java/com/swmansion/rnscreens/ScreenViewManager.kt:390:51 'class MapBuilder : Any' is deprecated. Deprecated in Java.
w: file:///home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/node_modules/react-native-screens/android/src/main/java/com/swmansion/rnscreens/ScreenWindowTraits.kt:55:42 'fun replaceSystemWindowInsets(p0: Int, p1: Int, p2: Int, p3: Int): WindowInsetsCompat' is deprecated. Deprecated in Java.
w: file:///home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/node_modules/react-native-screens/android/src/main/java/com/swmansion/rnscreens/ScreenWindowTraits.kt:56:39 'val systemWindowInsetLeft: Int' is deprecated. Deprecated in Java.
w: file:///home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/node_modules/react-native-screens/android/src/main/java/com/swmansion/rnscreens/ScreenWindowTraits.kt:58:39 'val systemWindowInsetRight: Int' is deprecated. Deprecated in Java.
w: file:///home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/node_modules/react-native-screens/android/src/main/java/com/swmansion/rnscreens/ScreenWindowTraits.kt:59:39 'val systemWindowInsetBottom: Int' is deprecated. Deprecated in Java.
w: file:///home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/node_modules/react-native-screens/android/src/main/java/com/swmansion/rnscreens/SearchBarManager.kt:5:8 'class MapBuilder : Any' is deprecated. Deprecated in Java.
w: file:///home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/node_modules/react-native-screens/android/src/main/java/com/swmansion/rnscreens/SearchBarManager.kt:142:9 'class MapBuilder : Any' is deprecated. Deprecated in Java.
w: file:///home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/node_modules/react-native-screens/android/src/main/java/com/swmansion/rnscreens/SearchBarManager.kt:144:13 'class MapBuilder : Any' is deprecated. Deprecated in Java.
w: file:///home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/node_modules/react-native-screens/android/src/main/java/com/swmansion/rnscreens/SearchBarManager.kt:146:13 'class MapBuilder : Any' is deprecated. Deprecated in Java.
w: file:///home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/node_modules/react-native-screens/android/src/main/java/com/swmansion/rnscreens/SearchBarManager.kt:148:13 'class MapBuilder : Any' is deprecated. Deprecated in Java.
w: file:///home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/node_modules/react-native-screens/android/src/main/java/com/swmansion/rnscreens/SearchBarManager.kt:150:13 'class MapBuilder : Any' is deprecated. Deprecated in Java.
w: file:///home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/node_modules/react-native-screens/android/src/main/java/com/swmansion/rnscreens/SearchBarManager.kt:152:13 'class MapBuilder : Any' is deprecated. Deprecated in Java.
w: file:///home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/node_modules/react-native-screens/android/src/main/java/com/swmansion/rnscreens/SearchBarManager.kt:154:13 'class MapBuilder : Any' is deprecated. Deprecated in Java.
w: file:///home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/node_modules/react-native-screens/android/src/main/java/com/swmansion/rnscreens/bottomsheet/BottomSheetDialogRootView.kt:7:8 'object ReactFeatureFlags : Any' is deprecated. Use com.facebook.react.internal.featureflags.ReactNativeFeatureFlags instead.
w: file:///home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/node_modules/react-native-screens/android/src/main/java/com/swmansion/rnscreens/bottomsheet/BottomSheetDialogRootView.kt:25:13 'object ReactFeatureFlags : Any' is deprecated. Use com.facebook.react.internal.featureflags.ReactNativeFeatureFlags instead.

> Task :react-native-gesture-handler:compileDebugJavaWithJavac
Note: /home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/node_modules/react-native-gesture-handler/android/paper/src/main/java/com/swmansion/gesturehandler/NativeRNGestureHandlerModuleSpec.java uses or overrides a deprecated API.
Note: Recompile with -Xlint:deprecation for details.

> Task :react-native-safe-area-context:compileDebugJavaWithJavac
Note: /home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/node_modules/react-native-safe-area-context/android/src/paper/java/com/th3rdwave/safeareacontext/NativeSafeAreaContextSpec.java uses or overrides a deprecated API.
Note: Recompile with -Xlint:deprecation for details.

> Task :app:stripWearDebugDebugSymbols
Unable to strip the following libraries, packaging them as they are: libc++_shared.so, libfbjni.so, libhermes.so, libhermestooling.so, libimagepipeline.so, libjsi.so, libnative-filters.so, libnative-imagetranscoder.so, libreactnative.so.

[Incubating] Problems report is available at: file:///home/wojtek/It_Projects/pomodoro-timerflow/frontend-apps/wear-app/PomodoroWear/android/build/reports/problems/problems-report.html

Deprecated Gradle features were used in this build, making it incompatible with Gradle 9.0.

You can use '--warning-mode all' to show the individual deprecation warnings and determine if they come from your own scripts or plugins.

For more on this, please refer to https://docs.gradle.org/8.12/userguide/command_line_interface.html#sec:command_line_warnings in the Gradle documentation.

BUILD SUCCESSFUL in 5m 12s
229 actionable tasks: 219 executed, 10 up-to-date

## Next Steps



build success!!


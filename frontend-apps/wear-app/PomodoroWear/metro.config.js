// Check if this already exists, if not create it with this content:
const { getDefaultConfig } = require('@react-native/metro-config');

const config = {
  resolver: {
    sourceExts: ['jsx', 'js', 'ts', 'tsx', 'json'],
  },
};

module.exports = getDefaultConfig(__dirname);
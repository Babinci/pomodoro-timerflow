// styles.js
import { StyleSheet } from 'react-native';

export const colors = {
  primary: '#7b68ee',
  secondary: '#5b4ee4',
  success: '#2ecd6f',
  danger: '#f65f6e',
  warning: '#ffb136',
  background: '#f7f6fb',
  card: '#ffffff',
  text: '#2b2c40',
  textLight: '#6f6b7d',
  border: '#dbdade',
};

export const styles = StyleSheet.create({
  // Layout
  container: {
    flex: 1,
    backgroundColor: colors.background,
    padding: 16,
  },
  content: {
    maxWidth: 800,
    width: '100%',
    alignSelf: 'center',
    gap: 24,
  },
  card: {
    backgroundColor: colors.card,
    borderRadius: 12,
    padding: 20,
    shadowColor: colors.text,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
    marginBottom: 16,
  },

  // Typography
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: colors.text,
    marginBottom: 16,
  },
  text: {
    fontSize: 16,
    color: colors.text,
  },
  smallText: {
    fontSize: 14,
    color: colors.textLight,
  },

  // Forms
  input: {
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: 8,
    padding: 12,
    marginBottom: 12,
    backgroundColor: 'white',
  },
  button: {
    backgroundColor: colors.primary,
    padding: 12,
    borderRadius: 8,
    alignItems: 'center',
  },
  buttonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: '600',
  },

  // Timer specific
  timerDisplay: {
    fontSize: 48,
    fontWeight: 'bold',
    color: colors.primary,
    textAlign: 'center',
  },
  timerContainer: {
    alignItems: 'center',
    marginBottom: 24,
  },

  // Task specific
  taskItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 16,
    backgroundColor: colors.background,
    borderRadius: 8,
    marginBottom: 8,
  },
  taskItemActive: {
    backgroundColor: '#f0edff',
    borderColor: colors.primary,
    borderWidth: 1,
  },
  dragHandle: {
    width: 20, 
    height: 20,
    marginRight: 8,
    alignItems: 'center',
    justifyContent: 'center',
  },
  taskItemWrapper: {
    position: 'relative',
    marginBottom: 8,
    cursor: 'grab',
  },

  // Settings specific
  settingsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 24,
  },
  settingsSection: {
    flex: 1,
    minWidth: 280,
  }
});

// Export both so components can use either styles or colors directly
export default { styles, colors };
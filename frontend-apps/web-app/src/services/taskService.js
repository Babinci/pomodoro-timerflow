import { apiConfig } from '../config/api';

/**
 * Updates the order of tasks on the server
 * @param {Array} newOrder - Array of task IDs in the new order
 * @param {string} token - Authentication token
 * @returns {Promise} - Promise that resolves with the response data
 */
export const updateTaskOrder = async (newOrder, token) => {
  try {
    const response = await fetch(`${apiConfig.baseUrl}/tasks/order`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        task_ids: newOrder
      })
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.error('Server error updating task order:', errorData);
      throw new Error('Failed to update task order');
    }

    return await response.json();
  } catch (error) {
    console.error('Error updating task order:', error);
    throw new Error('Failed to update task order');
  }
};

/**
 * Saves the task order to localStorage for persistence
 * @param {Array} orderedTasks - Array of task objects in the new order
 */
export const saveTaskOrderLocally = (orderedTasks) => {
  const orderMap = {};
  orderedTasks.forEach((task, index) => {
    orderMap[task.id] = index;
  });
  localStorage.setItem('taskOrder', JSON.stringify(orderMap));
}; 
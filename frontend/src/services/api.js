import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

// Chat API
export const sendChatMessage = async (message) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/chat/`, {
      message: message
    });
    return response.data;
  } catch (error) {
    console.error('Chat API Error:', error);
    throw error;
  }
};

// Workflow APIs
export const getMachineStatus = async (machineId) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/workflow/machine/${machineId}`);
    return response.data;
  } catch (error) {
    console.error('Machine Status API Error:', error);
    throw error;
  }
};

export const getOrderStatus = async (orderId) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/workflow/order/${orderId}`);
    return response.data;
  } catch (error) {
    console.error('Order Status API Error:', error);
    throw error;
  }
};

export const getSafetyAlerts = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/workflow/safety`);
    return response.data;
  } catch (error) {
    console.error('Safety Alerts API Error:', error);
    throw error;
  }
};

// Batch API
export const sendBatchQueries = async (messages) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/batch/multi`, {
      messages: messages
    });
    return response.data;
  } catch (error) {
    console.error('Batch API Error:', error);
    throw error;
  }
};

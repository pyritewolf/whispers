import { writable } from "svelte/store";

const messageStore = writable([]);

const sendMessage = (message, socket) => {
  if (socket.readyState <= 1) {
    socket.send(message);
  }
};

export default {
  subscribe: messageStore.subscribe,
  update: messageStore.update,
  sendMessage,
};

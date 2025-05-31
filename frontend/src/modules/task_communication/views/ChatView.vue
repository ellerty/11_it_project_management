<template>
  <BaseLayout>
    <div class="chat-container">
      <div ref="chatMessagesRef" class="chat-messages">
        <div
          v-for="(message, index) in messages"
          :key="index"
          :class="[
            'message',
            message.sender === '我' ? 'my-message' : 'other-message',
          ]"
        >
          <span class="sender" v-if="message.sender !== '我'">
            {{ message.sender }}:
          </span>
          <span class="text">{{ message.text }}</span>
        </div>
      </div>
      <div class="chat-input">
        <input v-model="newMessage" type="text" placeholder="输入消息..." />
        <button @click="sendMessage">发送</button>
      </div>
    </div>
  </BaseLayout>
</template>

<script>
import { ref, onMounted, nextTick } from 'vue';
import BaseLayout from '../../../components/BaseLayout.vue';

export default {
  name: 'ChatView',
  components: { BaseLayout },
  setup() {
    const chatMessagesRef = ref(null);

    const scrollToBottom = () => {
      if (chatMessagesRef.value) {
        chatMessagesRef.value.scrollTop = chatMessagesRef.value.scrollHeight;
      }
    };

    onMounted(() => {
      nextTick(() => {
        scrollToBottom();
      });
    });

    return {
      chatMessagesRef,
      scrollToBottom,
    };
  },
  data() {
    return {
      messages: [],
      newMessage: '',
    };
  },
  methods: {
    sendMessage() {
      if (this.newMessage.trim()) {
        this.messages.push({ sender: '我', text: this.newMessage });
        this.newMessage = '';
        this.scrollToBottom();
      }
    },
  },
};
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 100px);
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}
.chat-messages {
  flex: 1;
  overflow-y: auto;
  border: 1px solid #ccc;
  padding: 20px;
  margin-bottom: 20px;
  background-color: #fff;
  border-radius: 8px;
  display: flex;
  flex-direction: column; /* 改为从上到下排列 */
}
.message {
  margin-bottom: 10px;
  display: flex;
  align-items: center;
}
.sender {
  font-weight: bold;
  margin-right: 5px;
}
.chat-input {
  display: flex;
  gap: 10px;
}
.chat-input input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 16px;
}
.chat-input button {
  padding: 10px 20px;
  background-color: #2c6e49;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}
.chat-input button:hover {
  background-color: #225539;
}
.my-message {
  justify-content: flex-end;
  text-align: right;
}
.other-message {
  justify-content: flex-start;
  text-align: left;
}
.text {
  max-width: 60%;
  word-wrap: break-word;
  padding: 10px;
  border-radius: 8px;
  background-color: #e0f7fa;
}
.my-message .text {
  background-color: #c8e6c9;
}
</style>

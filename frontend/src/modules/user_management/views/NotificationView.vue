<template>
  <div class="notification-container">
    <div class="wechat-style-list">
      <div 
        v-for="(item, index) in notifications" 
        :key="index"
        class="message-item"
        :class="{ 'unread': item.unreadCount > 0 }"
      >
        <div class="avatar-container">
          <img :src="item.avatar" class="user-avatar" />
          <span v-if="item.unreadCount > 0" class="unread-badge">{{ item.unreadCount }}</span>
        </div>
        <div class="message-content">
          <div class="message-header">
            <span class="message-title">{{ item.title }}</span>
            <span class="message-time">{{ item.time }}</span>
          </div>
          <div class="message-preview">
            {{ item.message }}
            <div class="message-actions">
              <button class="action-btn">···</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const notifications = ref([
  {
    title: '系统通知',
    message: '您的简历已通过审核',
    time: '2023-05-15 10:30',
    avatar: 'https://api.dicebear.com/7.x/bottts/svg?seed=system',
    unreadCount: 2
  },
  {
    title: '新消息',
    message: '您有一个新的工作邀请',
    time: '2023-05-14 15:45',
    avatar: 'https://api.dicebear.com/7.x/bottts/svg?seed=message',
    unreadCount: 0
  },
  {
    title: '任务提醒',
    message: '您有一个新的任务待处理',
    time: '2023-05-14 09:20',
    avatar: 'https://api.dicebear.com/7.x/bottts/svg?seed=task',
    unreadCount: 1
  }
]);
</script>

<style scoped>
.notification-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  text-align: center;
  margin-bottom: 30px;
}

.wechat-style-list {
  display: flex;
  flex-direction: column;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.notification-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.notification-item {
  background: var(--white);
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.notification-title {
  font-weight: bold;
  margin-bottom: 5px;
}

.notification-message {
  color: #666;
  margin-bottom: 5px;
}

.notification-time {
  font-size: 12px;
  color: #999;
  text-align: right;
}

.message-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  background: var(--white);
  border-bottom: 1px solid var(--border-color);
  position: relative;
  cursor: pointer;
  transition: background-color 0.2s ease;

  &:hover {
    background-color: #f5f5f5;
  }

  .avatar-container {
    position: relative;
    margin-right: 15px;

    .user-avatar {
      width: 48px;
      height: 48px;
      border-radius: 4px;
      object-fit: cover;
      background-color: #f0f0f0;
    }

    .unread-badge {
      position: absolute;
      top: -6px;
      right: -6px;
      background: var(--danger-color);
      color: var(--white);
      border-radius: 10px;
      padding: 2px 6px;
      font-size: 12px;
    }
  }

  .message-content {
    flex: 1;

    .message-header {
      display: flex;
      justify-content: space-between;
      margin-bottom: 4px;

      .message-title {
        font-weight: 500;
        color: var(--text-color);
      }

      .message-time {
        font-size: 12px;
        color: var(--text-light);
      }
    }

    .message-preview {
      display: flex;
      justify-content: space-between;
      font-size: 14px;
      color: var(--text-light);

      .message-actions {
        .action-btn {
          border: none;
          background: none;
          color: var(--text-light);
          padding: 0 6px;
        }
      }
    }
  }
}

.unread {
  background-color: var(--background-color);

  .message-title {
    font-weight: 600 !important;
  }
}
</style>
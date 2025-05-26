<template>
  <!-- 基本信息编辑模态框 -->
  <div v-if="showBasicInfoModal" class="modal-overlay">
    <div class="modal-dialog">
      <div class="modal-header">
        <h3>编辑基本信息</h3>
        <button class="close-btn" @click="closeBasicInfoModal">&times;</button>
      </div>
      <div class="modal-body">
        <div class="form-group">
          <label for="edit-username" class="form-label">用户名</label>
          <input 
            type="text" 
            id="edit-username" 
            class="form-input" 
            v-model="editingProfile.username" 
            placeholder="请输入用户名"
          />
        </div>
        <div class="form-group">
          <label for="edit-email" class="form-label">电子邮箱</label>
          <input 
            type="email" 
            id="edit-email" 
            class="form-input" 
            v-model="editingProfile.email" 
            placeholder="请输入电子邮箱"
          />
        </div>
        <div class="form-group">
          <label for="edit-phone" class="form-label">手机号码</label>
          <input 
            type="tel" 
            id="edit-phone" 
            class="form-input" 
            v-model="editingProfile.phone" 
            placeholder="请输入手机号码"
          />
        </div>
      </div>
      <div class="modal-footer">
        <button class="btn btn-secondary" @click="closeBasicInfoModal">取消</button>
        <button class="btn btn-primary" @click="saveBasicInfo">保存</button>
      </div>
    </div>
  </div>
  
  <!-- 个人简介编辑模态框 -->
  <div v-if="showBioModal" class="modal-overlay">
    <div class="modal-dialog">
      <div class="modal-header">
        <h3>编辑个人简介</h3>
        <button class="close-btn" @click="closeBioModal">&times;</button>
      </div>
      <div class="modal-body">
        <div class="form-group">
          <label for="edit-bio" class="form-label">个人简介</label>
          <textarea 
            id="edit-bio" 
            class="form-textarea" 
            v-model="editingProfile.bio" 
            placeholder="请输入您的个人简介"
            rows="6"
          ></textarea>
        </div>
      </div>
      <div class="modal-footer">
        <button class="btn btn-secondary" @click="closeBioModal">取消</button>
        <button class="btn btn-primary" @click="saveBio">保存</button>
      </div>
    </div>
  </div>
  
  <!-- 技能编辑模态框 -->
  <div v-if="showSkillsModal" class="modal-overlay">
    <div class="modal-dialog">
      <div class="modal-header">
        <h3>编辑技能与专长</h3>
        <button class="close-btn" @click="closeSkillsModal">&times;</button>
      </div>
      <div class="modal-body">
        <div class="form-group">
          <label class="form-label">已添加的技能</label>
          <div class="skills-edit-list">
            <div 
              v-for="(skill, index) in editingProfile.skills" 
              :key="index" 
              class="skill-edit-item"
            >
              <span class="skill-name">{{ skill }}</span>
              <button class="remove-skill-btn" @click="removeSkill(index)">&times;</button>
            </div>
          </div>
        </div>
        <div class="form-group">
          <label for="new-skill" class="form-label">添加新技能</label>
          <div class="add-skill-group">
            <input 
              type="text" 
              id="new-skill" 
              class="form-input" 
              v-model="newSkill" 
              placeholder="请输入技能名称"
              @keyup.enter="addSkill"
            />
            <button class="btn btn-sm" @click="addSkill">添加</button>
          </div>
          <p class="form-hint">按回车键或点击添加按钮添加技能</p>
        </div>
      </div>
      <div class="modal-footer">
        <button class="btn btn-secondary" @click="closeSkillsModal">取消</button>
        <button class="btn btn-primary" @click="saveSkills">保存</button>
      </div>
    </div>
  </div>
  
  <!-- 企业信息编辑模态框 -->
  <div v-if="showCompanyInfoModal" class="modal-overlay">
    <div class="modal-dialog">
      <div class="modal-header">
        <h3>编辑企业信息</h3>
        <button class="close-btn" @click="closeCompanyInfoModal">&times;</button>
      </div>
      <div class="modal-body">
        <div class="form-group">
          <label for="edit-company-name" class="form-label">企业名称</label>
          <input 
            type="text" 
            id="edit-company-name" 
            class="form-input" 
            v-model="editingCompany.name" 
            placeholder="请输入企业名称"
          />
        </div>
        <div class="form-group">
          <label for="edit-company-industry" class="form-label">所属行业</label>
          <input 
            type="text" 
            id="edit-company-industry" 
            class="form-input" 
            v-model="editingCompany.industry" 
            placeholder="请输入所属行业"
          />
        </div>
        <div class="form-group">
          <label for="edit-company-address" class="form-label">企业地址</label>
          <input 
            type="text" 
            id="edit-company-address" 
            class="form-input" 
            v-model="editingCompany.address" 
            placeholder="请输入企业地址"
          />
        </div>
        <div class="form-group">
          <label for="edit-company-size" class="form-label">企业规模</label>
          <select 
            id="edit-company-size" 
            class="form-input" 
            v-model="editingCompany.size"
          >
            <option value="">请选择</option>
            <option value="少于50人">少于50人</option>
            <option value="50-200人">50-200人</option>
            <option value="200-500人">200-500人</option>
            <option value="500-1000人">500-1000人</option>
            <option value="1000人以上">1000人以上</option>
          </select>
        </div>
      </div>
      <div class="modal-footer">
        <button class="btn btn-secondary" @click="closeCompanyInfoModal">取消</button>
        <button class="btn btn-primary" @click="saveCompanyInfo">保存</button>
      </div>
    </div>
  </div>
  
  <!-- 企业简介编辑模态框 -->
  <div v-if="showCompanyBioModal" class="modal-overlay">
    <div class="modal-dialog">
      <div class="modal-header">
        <h3>编辑企业简介</h3>
        <button class="close-btn" @click="closeCompanyBioModal">&times;</button>
      </div>
      <div class="modal-body">
        <div class="form-group">
          <label for="edit-company-desc" class="form-label">企业简介</label>
          <textarea 
            id="edit-company-desc" 
            class="form-textarea" 
            v-model="editingCompany.description" 
            placeholder="请介绍企业文化、发展愿景等信息"
            rows="6"
          ></textarea>
        </div>
      </div>
      <div class="modal-footer">
        <button class="btn btn-secondary" @click="closeCompanyBioModal">取消</button>
        <button class="btn btn-primary" @click="saveCompanyBio">保存</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, defineProps, defineEmits, watchEffect } from 'vue';
import { updateUserProfile } from '../../../../services/authService';
import api from '../../../../services/api';

const props = defineProps({
  userProfile: {
    type: Object,
    required: true
  },
  showBasicInfoModal: Boolean,
  showBioModal: Boolean,
  showSkillsModal: Boolean,
  showCompanyInfoModal: Boolean,
  showCompanyBioModal: Boolean
});

const emits = defineEmits([
  'update:showBasicInfoModal',
  'update:showBioModal',
  'update:showSkillsModal',
  'update:showCompanyInfoModal',
  'update:showCompanyBioModal',
  'update:userProfile'
]);

// 编辑中的数据
const editingProfile = reactive({
  username: '',
  email: '',
  phone: '',
  bio: '',
  skills: []
});

const editingCompany = reactive({
  name: '',
  industry: '',
  address: '',
  size: '',
  description: ''
});

// 新技能
const newSkill = ref('');

// 监听 props 变化，更新编辑数据
watchEffect(() => {
  if (props.showBasicInfoModal) {
    editingProfile.username = props.userProfile.username || '';
    editingProfile.email = props.userProfile.email || '';
    editingProfile.phone = props.userProfile.phone || '';
  }
  
  if (props.showBioModal) {
    editingProfile.bio = props.userProfile.bio || '';
  }
  
  if (props.showSkillsModal) {
    editingProfile.skills = [...(props.userProfile.skills || [])];
  }
  
  if (props.showCompanyInfoModal) {
    editingCompany.name = props.userProfile.company?.name || '';
    editingCompany.industry = props.userProfile.company?.industry || '';
    editingCompany.address = props.userProfile.company?.address || '';
    editingCompany.size = props.userProfile.company?.size || '';
  }
  
  if (props.showCompanyBioModal) {
    editingCompany.description = props.userProfile.company?.description || '';
  }
});

// 关闭模态框
const closeBasicInfoModal = () => {
  emits('update:showBasicInfoModal', false);
};

const closeBioModal = () => {
  emits('update:showBioModal', false);
};

const closeSkillsModal = () => {
  emits('update:showSkillsModal', false);
  newSkill.value = '';
};

const closeCompanyInfoModal = () => {
  emits('update:showCompanyInfoModal', false);
};

const closeCompanyBioModal = () => {
  emits('update:showCompanyBioModal', false);
};

// 保存数据
const saveBasicInfo = async () => {
  try {
    // 准备要更新的数据
    const profileData = {
      username: editingProfile.username,
      email: editingProfile.email,
      phone: editingProfile.phone
    };
    
    // 调用API保存到数据库
    await updateUserProfile(profileData);
    
    // 更新本地状态
    props.userProfile.username = editingProfile.username;
    props.userProfile.email = editingProfile.email;
    props.userProfile.phone = editingProfile.phone;
    
    // 通知父组件更新
    emits('update:userProfile', { ...props.userProfile });
    
    // 关闭模态框
    closeBasicInfoModal();
    
    // 提示用户
    alert('基本信息保存成功');
  } catch (error) {
    console.error('保存基本信息失败:', error);
    alert('保存失败，请稍后重试');
  }
};

const saveBio = async () => {
  try {
    // 调用API保存到数据库
    await updateUserProfile({
      bio: editingProfile.bio
    });
    
    // 更新本地状态
    props.userProfile.bio = editingProfile.bio;
    
    // 通知父组件更新
    emits('update:userProfile', { ...props.userProfile });
    
    // 关闭模态框
    closeBioModal();
    
    // 提示用户
    alert('个人简介保存成功');
  } catch (error) {
    console.error('保存个人简介失败:', error);
    alert('保存失败，请稍后重试');
  }
};

// 技能相关操作
const addSkill = () => {
  if (!newSkill.value.trim()) return;
  
  // 检查是否已存在该技能
  if (!editingProfile.skills.includes(newSkill.value.trim())) {
    editingProfile.skills.push(newSkill.value.trim());
  }
  
  newSkill.value = '';
};

const removeSkill = (index) => {
  editingProfile.skills.splice(index, 1);
};

const saveSkills = async () => {
  try {
    // 调用API保存到数据库
    await updateUserProfile({
      skills: editingProfile.skills.join(',')
    });
    
    // 更新本地状态
    props.userProfile.skills = [...editingProfile.skills];
    
    // 通知父组件更新
    emits('update:userProfile', { ...props.userProfile });
    
    // 关闭模态框
    closeSkillsModal();
    
    // 提示用户
    alert('技能更新成功');
  } catch (error) {
    console.error('保存技能失败:', error);
    alert('保存失败，请稍后重试');
  }
};

// 企业信息相关
const saveCompanyInfo = async () => {
  try {
    // 调用API保存到数据库
    await api.put('auth/company/info/', {
      name: editingCompany.name,
      industry: editingCompany.industry,
      address: editingCompany.address,
      size: editingCompany.size
    });
    
    // 确保company对象存在
    if (!props.userProfile.company) {
      props.userProfile.company = {};
    }
    
    // 更新本地状态
    props.userProfile.company.name = editingCompany.name;
    props.userProfile.company.industry = editingCompany.industry;
    props.userProfile.company.address = editingCompany.address;
    props.userProfile.company.size = editingCompany.size;
    
    // 通知父组件更新
    emits('update:userProfile', { ...props.userProfile });
    
    // 关闭模态框
    closeCompanyInfoModal();
    
    // 提示用户
    alert('企业信息保存成功');
  } catch (error) {
    console.error('保存企业信息失败:', error);
    alert('保存失败，请稍后重试');
  }
};

const saveCompanyBio = async () => {
  try {
    // 调用API保存到数据库
    await api.put('auth/company/description/', {
      description: editingCompany.description
    });
    
    // 确保company对象存在
    if (!props.userProfile.company) {
      props.userProfile.company = {};
    }
    
    // 更新本地状态
    props.userProfile.company.description = editingCompany.description;
    
    // 通知父组件更新
    emits('update:userProfile', { ...props.userProfile });
    
    // 关闭模态框
    closeCompanyBioModal();
    
    // 提示用户
    alert('企业简介保存成功');
  } catch (error) {
    console.error('保存企业简介失败:', error);
    alert('保存失败，请稍后重试');
  }
};
</script>

<style scoped>
/* 模态窗样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-dialog {
  background-color: var(--white);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow-lg);
  width: 90%;
  max-width: 500px;
  overflow: hidden;
}

.modal-header {
  padding: 1rem;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  line-height: 1;
  color: var(--text-light);
  cursor: pointer;
}

.modal-body {
  padding: 1.5rem;
}

.modal-footer {
  padding: 1rem;
  border-top: 1px solid var(--border-color);
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

/* 表单样式 */
.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--text-color);
}

.form-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  font-size: 1rem;
  transition: border-color 0.2s;
}

.form-input:focus {
  border-color: var(--accent-color);
  outline: none;
}

.form-textarea {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  font-size: 1rem;
  transition: border-color 0.2s;
  resize: vertical;
}

.form-textarea:focus {
  border-color: var(--accent-color);
  outline: none;
}

.form-hint {
  margin-top: 0.5rem;
  font-size: 0.85rem;
  color: var(--text-light);
}

/* 技能编辑样式 */
.skills-edit-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.skill-edit-item {
  display: flex;
  align-items: center;
  background-color: var(--primary-light);
  padding: 0.3rem 0.6rem;
  border-radius: 2rem;
}

.skill-name {
  margin-right: 0.3rem;
}

.remove-skill-btn {
  background: none;
  border: none;
  color: var(--text-light);
  font-size: 1.1rem;
  cursor: pointer;
  padding: 0 0.2rem;
  line-height: 1;
}

.add-skill-group {
  display: flex;
  gap: 0.5rem;
}

.btn-sm {
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
}
</style> 
<template>
  <BaseLayout>
    <div class="profile-container">
      <!-- 用户类型切换 -->
      <ModeSwitch
        :user-mode="userMode"
        @update:user-mode="userMode = $event"
      />
      
      <!-- 个人资料卡片 -->
      <div class="profile-card">
        <!-- 用户基本信息 -->
        <ProfileHeader
          :user-profile="userProfile"
          @edit-basic-info="showBasicInfoModal = true"
        />
        
        <!-- 零工模式下的内容 -->
        <div v-if="userMode === 'freelancer'" class="freelancer-content">
          <FreelancerSkills
            :skills="userProfile.skills"
            @edit-skills="showSkillsModal = true"
          />
          
          <FreelancerBio
            :bio="userProfile.bio"
            @edit-bio="showBioModal = true"
          />
          
          <!-- 证书组件 -->
          <FreelancerCertificates
            :certificates="userProfile.certificates"
            @add-certificate="showCertUploadModal = true"
            @view-certificate="viewCertificate"
          />
          
          <!-- 工作经历组件 -->
          <FreelancerExperience
            :experiences="userProfile.experiences"
            @add-experience="showAddExperienceModal = true"
          />
          
          <!-- 实名认证组件 -->
          <FreelancerVerification
            :verification-status="userProfile.realNameStatus"
            :real-name="userProfile.realName"
            :verify-time="userProfile.verifyTime"
            :verify-submit-time="userProfile.verifySubmitTime"
            :verify-fail-reason="userProfile.verifyFailReason"
            :real-name-verified="userProfile.realNameVerified"
            @show-verify-form="showVerifyFormModal = true"
          />
        </div>
        
        <!-- 招聘模式下的内容 -->
        <div v-else class="employer-content">
          <!-- 企业信息组件 -->
          <EmployerCompanyInfo
            :company="userProfile.company"
            @edit-company-info="showCompanyInfoModal = true"
          />
          
          <!-- 企业简介组件 -->
          <EmployerBio
            :company="userProfile.company"
            @edit-company-bio="showCompanyBioModal = true"
          />
          
          <!-- 企业资质组件 -->
          <EmployerCertificates
            :company="userProfile.company"
            @add-certificate="showCompanyCertUploadModal = true"
            @view-certificate="viewCompanyCertificate"
          />
          
          <!-- 招聘偏好组件 -->
          <EmployerPreferences
            :preferences="userProfile.recruitmentPreferences"
            @edit-preferences="showRecruitmentPrefsModal = true"
          />
        </div>
      </div>
    </div>
    
    <!-- 模态框组件 -->
    <ProfileModals
      :user-profile="userProfile"
      :show-basic-info-modal="showBasicInfoModal"
      :show-bio-modal="showBioModal"
      :show-skills-modal="showSkillsModal"
      :show-company-info-modal="showCompanyInfoModal"
      :show-company-bio-modal="showCompanyBioModal"
      @update:show-basic-info-modal="showBasicInfoModal = $event"
      @update:show-bio-modal="showBioModal = $event"
      @update:show-skills-modal="showSkillsModal = $event"
      @update:show-company-info-modal="showCompanyInfoModal = $event"
      @update:show-company-bio-modal="showCompanyBioModal = $event"
      @update:user-profile="handleProfileUpdate"
    />
    
    <!-- 证书上传模态框 -->
    <div v-if="showCertUploadModal" class="modal-overlay">
      <div class="modal-dialog">
        <div class="modal-header">
          <h3>上传证书</h3>
          <button class="close-btn" @click="showCertUploadModal = false">&times;</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label for="cert-name" class="form-label">证书名称</label>
            <input 
              type="text" 
              id="cert-name" 
              class="form-input" 
              v-model="newCertificate.name" 
              placeholder="请输入证书名称"
            />
          </div>
          <div class="form-group">
            <label for="cert-issue-date" class="form-label">发证日期</label>
            <input 
              type="date" 
              id="cert-issue-date" 
              class="form-input" 
              v-model="newCertificate.issueDate"
            />
          </div>
          <div class="form-group">
            <label for="cert-file" class="form-label">证书文件</label>
              <input 
                type="file" 
                id="cert-file" 
              @change="handleCertificateFileChange" 
                accept=".pdf,.jpg,.jpeg,.png"
              class="form-input" 
            />
            <p class="form-hint">支持PDF、JPG、PNG格式，文件大小不超过5MB</p>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="showCertUploadModal = false">取消</button>
          <button class="btn btn-primary" @click="uploadCertificate">上传</button>
        </div>
      </div>
    </div>
    
    <!-- 工作经历添加模态框 -->
    <div v-if="showAddExperienceModal" class="modal-overlay">
      <div class="modal-dialog">
        <div class="modal-header">
          <h3>添加工作经历</h3>
          <button class="close-btn" @click="showAddExperienceModal = false">&times;</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label for="exp-title" class="form-label">职位名称</label>
            <input 
              type="text" 
              id="exp-title" 
              class="form-input" 
              v-model="newExperience.title" 
              placeholder="请输入职位名称"
            />
          </div>
          <div class="form-group">
            <label for="exp-company" class="form-label">公司名称</label>
            <input 
              type="text" 
              id="exp-company" 
              class="form-input" 
              v-model="newExperience.company" 
              placeholder="请输入公司名称"
            />
          </div>
          <div class="form-group">
            <label for="exp-start-date" class="form-label">开始日期</label>
            <input 
              type="date" 
              id="exp-start-date" 
              class="form-input" 
              v-model="newExperience.startDate"
            />
          </div>
          <div class="form-group">
            <div class="form-checkbox">
              <input 
                type="checkbox" 
                id="exp-is-current" 
                v-model="newExperience.isCurrent" 
              />
              <label for="exp-is-current">当前工作</label>
            </div>
          </div>
          <div class="form-group" v-if="!newExperience.isCurrent">
            <label for="exp-end-date" class="form-label">结束日期</label>
            <input 
              type="date" 
              id="exp-end-date" 
              class="form-input" 
              v-model="newExperience.endDate"
            />
          </div>
          <div class="form-group">
            <label for="exp-description" class="form-label">工作描述</label>
            <textarea 
              id="exp-description" 
              class="form-textarea" 
              v-model="newExperience.description" 
              placeholder="请描述您的工作职责和成就"
              rows="4"
            ></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="showAddExperienceModal = false">取消</button>
          <button class="btn btn-primary" @click="addExperience">添加</button>
        </div>
      </div>
    </div>
    
    <!-- 实名认证表单模态框 -->
    <div v-if="showVerifyFormModal" class="modal-overlay">
      <div class="modal-dialog">
        <div class="modal-header">
          <h3>实名认证</h3>
          <button class="close-btn" @click="showVerifyFormModal = false">&times;</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label for="real-name" class="form-label">真实姓名</label>
            <input 
              type="text" 
              id="real-name" 
              class="form-input" 
              v-model="verifyForm.realName" 
              placeholder="请输入您的真实姓名"
            />
          </div>
          <div class="form-group">
            <label for="id-number" class="form-label">身份证号码</label>
            <input 
              type="text" 
              id="id-number" 
              class="form-input" 
              v-model="verifyForm.idNumber" 
              placeholder="请输入您的身份证号码"
            />
          </div>
          <div class="form-group">
            <label for="id-front" class="form-label">身份证正面照片</label>
                <input 
                  type="file" 
                  id="id-front" 
              @change="handleIdFrontChange" 
                  accept="image/*"
              class="form-input" 
                />
              </div>
          <div class="form-group">
            <label for="id-back" class="form-label">身份证背面照片</label>
                <input 
                  type="file" 
                  id="id-back" 
              @change="handleIdBackChange" 
                  accept="image/*"
              class="form-input" 
                />
              </div>
          <p class="form-hint">请上传清晰的身份证照片，确保信息可见且照片边缘完整</p>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="showVerifyFormModal = false">取消</button>
          <button class="btn btn-primary" @click="submitVerification">提交认证</button>
        </div>
      </div>
    </div>
  </BaseLayout>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import BaseLayout from '../../../components/BaseLayout.vue';
import { authStore } from '../../../store/authStore';
import { getUserProfile } from '../../../services/authService';
import api from '../../../services/api';

// 导入拆分后的组件
import ModeSwitch from '../components/ModeSwitch.vue';
import ProfileHeader from '../components/ProfileHeader.vue';
import FreelancerSkills from '../components/FreelancerSkills.vue';
import FreelancerBio from '../components/FreelancerBio.vue';
import FreelancerCertificates from '../components/FreelancerCertificates.vue';
import FreelancerExperience from '../components/FreelancerExperience.vue';
import FreelancerVerification from '../components/FreelancerVerification.vue';
import EmployerCompanyInfo from '../components/EmployerCompanyInfo.vue';
import EmployerBio from '../components/EmployerBio.vue';
import EmployerCertificates from '../components/EmployerCertificates.vue';
import EmployerPreferences from '../components/EmployerPreferences.vue';
import ProfileModals from '../components/ProfileModals.vue';

// 用户模式 - 'freelancer'(零工用户) 或 'employer'(招聘用户)
const userMode = ref('freelancer');

// 模态框显示状态
const showBasicInfoModal = ref(false);
const showBioModal = ref(false);
const showSkillsModal = ref(false);
const showCertUploadModal = ref(false);
const showAddExperienceModal = ref(false);
const showVerifyFormModal = ref(false);
const showCompanyInfoModal = ref(false);
const showCompanyBioModal = ref(false);
const showCompanyCertUploadModal = ref(false);
const showRecruitmentPrefsModal = ref(false);

// 用户资料数据
const userProfile = reactive({
  username: '',
  email: '',
  phone: '',
  avatar: null,
  bio: '',
  creditScore: 0,
  realNameVerified: false,
  realName: '',
  verifyTime: '',
  realNameStatus: '',
  verifySubmitTime: '',
  verifyFailReason: '',
  certificationStatus: '',
  skills: [],
  certificates: [],
  experiences: [],
  company: {
    name: '',
    logo: null,
    verifyStatus: '',
    industry: '',
    address: '',
    size: '',
    description: '',
    certificates: []
  },
  recruitmentPreferences: {
    positions: [],
    locations: [],
    salaryMin: 0,
    salaryMax: 0,
    requirements: ''
  }
});

// 新增状态
const newCertificate = reactive({
  name: '',
  issueDate: '',
  certificateFile: null
});

const newExperience = reactive({
  title: '',
  company: '',
  startDate: '',
  endDate: '',
  isCurrent: false,
  description: ''
});

const verifyForm = reactive({
  realName: '',
  idNumber: '',
  idFront: null,
  idBack: null
});

// 页面加载时获取用户资料
onMounted(async () => {
  try {
    // 从 authStore 获取当前用户信息
    const user = authStore.state.user;
    
    if (user) {
      // 如果用户已登录，尝试从 authService 获取完整资料
      try {
        const profileData = await getUserProfile();
        
        // 处理skills字段 - 确保转换为数组格式
        if (profileData.skills && typeof profileData.skills === 'string') {
          profileData.skills = profileData.skills.split(',').filter(skill => skill.trim() !== '');
        } else if (!profileData.skills) {
          profileData.skills = [];
        }
        
        // 处理certificates字段 - 确保是数组
        if (!profileData.certificates) {
          profileData.certificates = [];
        } else if (profileData.certificates) {
          // 确保证书数据格式兼容前端组件
          profileData.certificates = profileData.certificates.map(cert => ({
            ...cert,
            issueDate: cert.issue_date || cert.issueDate,
            verifyStatus: cert.verify_status || cert.verifyStatus || 'pending'
          }));
        }
        
        // 处理实名认证信息
        if (profileData.identity_verification) {
          // 将API返回的认证信息映射到组件需要的字段名
          profileData.realName = profileData.identity_verification.real_name || '';
          profileData.realNameStatus = profileData.identity_verification.verify_status || 'unverified';
          profileData.verifyTime = profileData.identity_verification.verify_time || '';
          profileData.verifySubmitTime = profileData.identity_verification.submit_time || '';
          profileData.verifyFailReason = profileData.identity_verification.verify_fail_reason || '';
          
          // 调试输出
          console.log('收到的实名认证信息:', profileData.identity_verification);
        }
        
        // 设置用户角色/模式
        if (profileData.role) {
          userMode.value = profileData.role;
        }
        
        // 合并基础用户信息和完整资料
        Object.assign(userProfile, {
          ...user,
          ...profileData
        });
        
        console.log('加载的用户资料:', userProfile);
      } catch (error) {
        console.error('获取完整资料失败，使用基本用户信息:', error);
        // 如果获取完整资料失败，只使用基础用户信息
        Object.assign(userProfile, user);
        
        // 确保skills字段是数组
        if (typeof userProfile.skills === 'string') {
          userProfile.skills = userProfile.skills.split(',').filter(skill => skill.trim() !== '');
        } else if (!userProfile.skills) {
          userProfile.skills = [];
        }
        
        // 确保certificates是数组
        if (!userProfile.certificates) {
          userProfile.certificates = [];
        }
      }
    }
  } catch (error) {
    console.error('获取用户资料失败:', error);
    // 可以在这里添加错误处理逻辑
  }
});

// 处理用户资料更新
const handleProfileUpdate = (updatedProfile) => {
  console.log('接收到更新的用户资料:', updatedProfile);
  
  // 更新组件状态
  Object.assign(userProfile, updatedProfile);
  
  // 确保localStorage中的用户信息也被更新
  const currentUser = JSON.parse(localStorage.getItem('user') || '{}');
  if (currentUser) {
    // 更新基本属性
    if (updatedProfile.username) currentUser.username = updatedProfile.username;
    if (updatedProfile.email) currentUser.email = updatedProfile.email;
    if (updatedProfile.phone) currentUser.phone = updatedProfile.phone;
    if (updatedProfile.bio) currentUser.bio = updatedProfile.bio;
    
    // 保存回localStorage
    localStorage.setItem('user', JSON.stringify(currentUser));
    console.log('已更新localStorage中的用户信息:', currentUser);
  }
};

// 查看证书
const viewCertificate = (cert) => {
  console.log('查看证书:', cert);
  alert(`查看证书: ${cert.name}`);
};

const viewCompanyCertificate = (cert) => {
  console.log('查看企业证书:', cert);
  alert(`查看企业证书: ${cert.name}`);
};

// 文件处理函数
const handleCertificateFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
  // 检查文件大小
  if (file.size > 5 * 1024 * 1024) {
    alert('文件大小不能超过5MB');
      event.target.value = '';
    return;
  }
  
  // 检查文件类型
    const allowedTypes = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png'];
    if (!allowedTypes.includes(file.type)) {
    alert('只支持PDF、JPG、PNG格式文件');
      event.target.value = '';
    return;
  }
  
    newCertificate.certificateFile = file;
  }
};

const handleIdFrontChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    verifyForm.idFront = file;
  }
};

const handleIdBackChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    verifyForm.idBack = file;
  }
};

// 提交函数
const uploadCertificate = async () => {
  // 表单验证
  if (!newCertificate.name || !newCertificate.issueDate || !newCertificate.certificateFile) {
    alert('请填写完整的证书信息');
    return;
  }
  
  // 创建FormData对象
    const formData = new FormData();
    formData.append('name', newCertificate.name);
    formData.append('issue_date', newCertificate.issueDate);
  formData.append('certificate_file', newCertificate.certificateFile);
    
  try {
    // 使用API服务
    const response = await api.post('auth/certificates/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    
    // 更新证书列表
    if (!userProfile.certificates) userProfile.certificates = [];
    
    // 确保添加的证书有正确的格式
    const newCert = {
      ...response.data,
      // 确保数据同时支持前端组件需要的格式和后端API返回的格式
      issueDate: response.data.issue_date || response.data.issueDate,
      verifyStatus: response.data.verify_status || response.data.verifyStatus || 'pending'
    };
    
    userProfile.certificates.push(newCert);
    
    // 保存更新的用户资料到localStorage，确保刷新后数据持久化
    const currentUser = JSON.parse(localStorage.getItem('user') || '{}');
    if (currentUser) {
      currentUser.certificates = userProfile.certificates;
      localStorage.setItem('user', JSON.stringify(currentUser));
    }
    
    // 重置表单
    newCertificate.name = '';
    newCertificate.issueDate = '';
    newCertificate.certificateFile = null;
    
    // 关闭模态框
    showCertUploadModal.value = false;
    
    alert('证书上传成功');
  } catch (error) {
    console.error('证书上传失败:', error);
    alert('证书上传失败，请稍后重试');
  }
};

const addExperience = async () => {
  // 表单验证
  if (!newExperience.title || !newExperience.company || !newExperience.startDate || (!newExperience.isCurrent && !newExperience.endDate) || !newExperience.description) {
    alert('请填写完整的工作经历信息');
    return;
  }
  
  try {
    // 准备数据
    const experienceData = {
      title: newExperience.title,
      company: newExperience.company,
      start_date: newExperience.startDate,
      end_date: newExperience.isCurrent ? null : newExperience.endDate,
      is_current: newExperience.isCurrent,
      description: newExperience.description
    };
    
    // 使用API服务
    const response = await api.post('auth/experiences/', experienceData);
    
    // 更新工作经历列表
    if (!userProfile.experiences) userProfile.experiences = [];
    userProfile.experiences.push(response.data);
    
    // 重置表单
    Object.assign(newExperience, {
      title: '',
      company: '',
      startDate: '',
      endDate: '',
      isCurrent: false,
      description: ''
    });
    
    // 关闭模态框
    showAddExperienceModal.value = false;
    
    alert('工作经历添加成功');
  } catch (error) {
    console.error('添加工作经历失败:', error);
    alert('添加工作经历失败，请稍后重试');
  }
};

const submitVerification = async () => {
  // 表单验证
  if (!verifyForm.realName || !verifyForm.idNumber || !verifyForm.idFront || !verifyForm.idBack) {
    alert('请填写完整的实名认证信息');
      return;
    }
    
  // 创建FormData对象
    const formData = new FormData();
    formData.append('real_name', verifyForm.realName);
    formData.append('id_number', verifyForm.idNumber);
    formData.append('id_front', verifyForm.idFront);
    formData.append('id_back', verifyForm.idBack);
    
  try {
    // 使用API服务
    const response = await api.post('auth/verify/identity/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    
    // 更新认证状态
    userProfile.realNameStatus = 'pending';
    userProfile.verifySubmitTime = new Date().toISOString().split('T')[0];
    
    // 重置表单
    Object.assign(verifyForm, {
      realName: '',
      idNumber: '',
      idFront: null,
      idBack: null
    });
    
    // 关闭模态框
    showVerifyFormModal.value = false;
    
    alert('实名认证信息已提交，请等待审核');
  } catch (error) {
    console.error('提交实名认证失败:', error);
    alert('提交实名认证失败，请稍后重试');
  }
};
</script>

<style scoped>
.profile-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 1rem;
}

.profile-card {
  background-color: var(--white);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow);
  overflow: hidden;
}

.freelancer-content, .employer-content {
  /* 通用内容样式 */
}

/* 模态框样式 */
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
  margin: 0 auto;
  animation: modal-appear 0.3s ease-out;
}

@keyframes modal-appear {
  from {
    opacity: 0;
    transform: translateY(-50px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
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
  font-size: 1.2rem;
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
  max-height: 70vh;
  overflow-y: auto;
}

.modal-footer {
  padding: 1rem;
  border-top: 1px solid var(--border-color);
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.form-input,
.form-textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  font-size: 1rem;
}

.form-textarea {
  resize: vertical;
}

.form-hint {
  margin-top: 0.5rem;
  font-size: 0.85rem;
  color: var(--text-light);
}

.form-checkbox {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: var(--border-radius);
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-primary {
  background-color: var(--primary-color);
  color: white;
}

.btn-primary:hover {
  background-color: var(--primary-dark);
}

.btn-secondary {
  background-color: var(--background-color);
  border: 1px solid var(--border-color);
}

.btn-secondary:hover {
  background-color: var(--border-color);
}
</style>
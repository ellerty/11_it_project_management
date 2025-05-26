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
    
    <!-- 其他模态框组件 -->
    <!-- ... 证书上传、工作经历添加等模态框 ... -->
    
  </BaseLayout>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import BaseLayout from '../../../components/BaseLayout.vue';
import { authStore } from '../../../store/authStore';
import { getUserProfile } from '../../../services/authService';

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
        
        // 设置用户角色/模式
        if (profileData.role) {
          userMode.value = profileData.role;
        }
        
        // 合并基础用户信息和完整资料
        Object.assign(userProfile, {
          ...user,
          ...profileData
        });
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
      }
    }
  } catch (error) {
    console.error('获取用户资料失败:', error);
    // 可以在这里添加错误处理逻辑
  }
});

// 处理用户资料更新
const handleProfileUpdate = (updatedProfile) => {
  Object.assign(userProfile, updatedProfile);
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
</style> 
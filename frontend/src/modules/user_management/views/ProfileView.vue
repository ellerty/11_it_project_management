<template>
  <BaseLayout>
    <div class="profile-container">
      <!-- 用户类型切换 -->
      <div class="user-mode-switch" :class="{'employer-mode': userMode === 'employer'}">
        <div class="current-mode">
          <span>当前模式：{{ userMode === 'freelancer' ? '零工用户' : '招聘用户' }}</span>
          <span class="mode-color" :class="{'freelancer': userMode === 'freelancer', 'employer': userMode === 'employer'}"></span>
        </div>
        <button @click="handleModeSwitch" class="btn mode-switch-btn" :class="{'btn-freelancer': userMode === 'employer', 'btn-employer': userMode === 'freelancer'}">
          切换至{{ userMode === 'freelancer' ? '招聘用户' : '零工用户' }}
        </button>
      </div>
      
      <!-- 个人资料卡片 -->
      <div class="profile-card">
        <div class="profile-header">
          <div class="avatar-section">
            <div class="avatar-container">
              <img v-if="userProfile.avatar" :src="userProfile.avatar" alt="用户头像" class="avatar" />
              <div v-else class="avatar-placeholder">{{ getInitials(userProfile.username) }}</div>
              <div class="avatar-upload">
                <label for="avatar-input" class="avatar-edit-btn">
                  <i class="edit-icon"></i>
                </label>
                <input id="avatar-input" type="file" accept="image/*" @change="handleAvatarChange" class="hidden" />
              </div>
            </div>
            <div class="credit-score" :class="getCreditScoreClass(userProfile.creditScore)">
              <span class="score-value">{{ userProfile.creditScore }}</span>
              <span class="score-label">信誉分</span>
            </div>
          </div>
          
          <div class="user-basic-info">
            <h2 class="username">{{ userProfile.username }}</h2>
            <div class="verify-badges">
              <span v-if="userProfile.realNameVerified" class="badge verified">
                <i class="verify-icon"></i> 实名已认证
              </span>
              <span v-else class="badge unverified">
                <i class="unverify-icon"></i> 实名未认证
              </span>
              
              <span v-if="userProfile.certificationStatus" :class="['badge', getCertificationClass(userProfile.certificationStatus)]">
                <i class="cert-icon"></i> {{ getCertificationText(userProfile.certificationStatus) }}
              </span>
            </div>
            <div class="contact-info">
              <div class="info-item">
                <i class="icon phone-icon"></i>
                <span>{{ maskPhone(userProfile.phone) }}</span>
              </div>
              <div class="info-item">
                <i class="icon email-icon"></i>
                <span>{{ maskEmail(userProfile.email) }}</span>
              </div>
            </div>
          </div>
          
          <div class="profile-actions">
            <button class="btn btn-outline" @click="initEditBasicInfo">
              <i class="edit-icon"></i> 编辑资料
            </button>
          </div>
        </div>
        
        <!-- 零工模式下的内容 -->
        <div v-if="userMode === 'freelancer'" class="freelancer-content">
          <div class="section-card">
            <div class="section-header">
              <h3>技能与专长</h3>
              <button class="btn-link" @click="initEditSkills">编辑</button>
            </div>
            <div class="skills-container">
              <div v-if="userProfile.skills && userProfile.skills.length > 0" class="skills-list">
                <span v-for="(skill, index) in userProfile.skills" :key="index" class="skill-tag">
                  {{ skill }}
                </span>
              </div>
              <div v-else class="empty-content">
                <p>您还没有添加技能，点击"编辑"按钮添加您的专业技能</p>
              </div>
            </div>
          </div>
          
          <div class="section-card">
            <div class="section-header">
              <h3>个人简介</h3>
              <button class="btn-link" @click="initEditBio">编辑</button>
            </div>
            <div class="bio-container">
              <p v-if="userProfile.bio">{{ userProfile.bio }}</p>
              <div v-else class="empty-content">
                <p>您还没有添加个人简介，点击"编辑"按钮介绍一下自己吧</p>
              </div>
            </div>
          </div>
          
          <div class="section-card">
            <div class="section-header">
              <h3>证书与资质</h3>
              <button class="btn-link" @click="showCertUpload = true">上传证书</button>
            </div>
            <div class="certificates-container">
              <div v-if="userProfile.certificates && userProfile.certificates.length > 0" class="cert-list">
                <div v-for="(cert, index) in userProfile.certificates" :key="index" class="cert-item">
                  <div class="cert-info">
                    <div class="cert-name">{{ cert.name }}</div>
                    <div class="cert-date">获得日期: {{ formatDate(cert.issueDate) }}</div>
                    <div :class="['cert-status', getCertStatusClass(cert.verifyStatus)]">
                      {{ getCertStatusText(cert.verifyStatus) }}
                    </div>
                  </div>
                  <div class="cert-actions">
                    <button class="btn-link" @click="viewCertificate(cert)">查看</button>
                  </div>
                </div>
              </div>
              <div v-else class="empty-content">
                <p>您还没有上传任何证书，上传专业证书可以提高您的信誉</p>
              </div>
            </div>
          </div>
          
          <div class="section-card">
            <div class="section-header">
              <h3>工作经历</h3>
              <button class="btn-link" @click="showAddExperience = true">添加经历</button>
            </div>
            <div class="experience-container">
              <div v-if="userProfile.experiences && userProfile.experiences.length > 0" class="experience-list">
                <div v-for="(exp, index) in userProfile.experiences" :key="index" class="exp-item">
                  <div class="exp-timeline">
                    <div class="exp-duration">{{ formatDateRange(exp.startDate, exp.endDate) }}</div>
                    <div class="exp-duration-line"></div>
                  </div>
                  <div class="exp-content">
                    <div class="exp-title">{{ exp.title }} @ {{ exp.company }}</div>
                    <div class="exp-description">{{ exp.description }}</div>
                  </div>
                </div>
              </div>
              <div v-else class="empty-content">
                <p>您还没有添加工作经历，添加经历可以让雇主更了解您</p>
              </div>
            </div>
          </div>
          
          <div class="section-card">
            <div class="section-header">
              <h3>实名认证</h3>
              <button v-if="!userProfile.realNameVerified" class="btn-link" @click="showVerifyForm = true">
                去认证
              </button>
            </div>
            <div class="verify-container">
              <div v-if="userProfile.realNameVerified" class="verify-info">
                <div class="verify-success">
                  <i class="icon-success"></i>
                  <span>您已完成实名认证</span>
                </div>
                <div class="verify-detail">
                  <p>认证姓名: {{ maskRealName(userProfile.realName) }}</p>
                  <p>认证时间: {{ formatDate(userProfile.verifyTime) }}</p>
                </div>
              </div>
              <div v-else-if="userProfile.realNameStatus === 'pending'" class="verify-info verify-pending">
                <div class="verify-status-pending">
                  <i class="icon-pending"></i>
                  <span>实名认证审核中</span>
                </div>
                <div class="verify-detail">
                  <p>认证姓名: {{ maskRealName(userProfile.realName) }}</p>
                  <p>提交时间: {{ formatDate(userProfile.verifySubmitTime) }}</p>
                  <p class="verify-note">您的实名认证信息已提交，请耐心等待审核</p>
                </div>
              </div>
              <div v-else-if="userProfile.realNameStatus === 'failed'" class="verify-info verify-failed">
                <div class="verify-status-failed">
                  <i class="icon-failed"></i>
                  <span>实名认证未通过</span>
                </div>
                <div class="verify-detail">
                  <p>失败原因: {{ userProfile.verifyFailReason || '信息有误，请重新提交' }}</p>
                  <button class="btn btn-outline" @click="showVerifyForm = true">重新认证</button>
                </div>
              </div>
              <div v-else class="empty-content">
                <p>您还未进行实名认证，实名认证可以提高接单率和信任度</p>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 招聘模式下的内容 -->
        <div v-else class="employer-content">
          <div class="section-card">
            <div class="section-header">
              <h3>企业信息</h3>
              <button class="btn-link" @click="initEditCompanyInfo">编辑</button>
            </div>
            <div class="company-container">
              <div v-if="userProfile.company && userProfile.company.name" class="company-info">
                <div class="company-logo-container">
                  <img v-if="userProfile.company.logo" :src="userProfile.company.logo" alt="公司Logo" class="company-logo" />
                  <div v-else class="company-logo-placeholder">{{ getInitials(userProfile.company.name) }}</div>
                </div>
                <div class="company-details">
                  <h4 class="company-name">{{ userProfile.company.name }}</h4>
                  <div :class="['company-verify-status', getCompanyVerifyClass(userProfile.company.verifyStatus)]">
                    {{ getCompanyVerifyText(userProfile.company.verifyStatus) }}
                  </div>
                  <div class="company-info-list">
                    <div class="company-info-item">
                      <i class="icon industry-icon"></i>
                      <span>行业: {{ userProfile.company.industry || '未设置' }}</span>
                    </div>
                    <div class="company-info-item">
                      <i class="icon location-icon"></i>
                      <span>地址: {{ userProfile.company.address || '未设置' }}</span>
                    </div>
                    <div class="company-info-item">
                      <i class="icon size-icon"></i>
                      <span>规模: {{ userProfile.company.size || '未设置' }}</span>
                    </div>
                  </div>
                </div>
              </div>
              <div v-else class="empty-content">
                <p>您还未添加企业信息，完善企业信息有助于吸引更多优质人才</p>
              </div>
            </div>
          </div>
          
          <div class="section-card">
            <div class="section-header">
              <h3>企业简介</h3>
              <button class="btn-link" @click="initEditCompanyBio">编辑</button>
            </div>
            <div class="company-bio-container">
              <p v-if="userProfile.company && userProfile.company.description">{{ userProfile.company.description }}</p>
              <div v-else class="empty-content">
                <p>您还未添加企业简介，介绍企业文化和发展愿景可以提高招聘效果</p>
              </div>
            </div>
          </div>
          
          <div class="section-card">
            <div class="section-header">
              <h3>企业资质认证</h3>
              <button class="btn-link" @click="showCompanyCertUpload = true">上传资质</button>
            </div>
            <div class="company-certificates-container">
              <div v-if="userProfile.company && userProfile.company.certificates && userProfile.company.certificates.length > 0" class="cert-list">
                <div v-for="(cert, index) in userProfile.company.certificates" :key="index" class="cert-item">
                  <div class="cert-info">
                    <div class="cert-name">{{ cert.name }}</div>
                    <div class="cert-date">有效期: {{ formatDateRange(cert.issueDate, cert.expiryDate) }}</div>
                    <div :class="['cert-status', getCertStatusClass(cert.verifyStatus)]">
                      {{ getCertStatusText(cert.verifyStatus) }}
                    </div>
                  </div>
                  <div class="cert-actions">
                    <button class="btn-link" @click="viewCompanyCertificate(cert)">查看</button>
                  </div>
                </div>
              </div>
              <div v-else class="empty-content">
                <p>您还未上传企业资质证明，上传资质证明可以提高企业可信度</p>
              </div>
            </div>
          </div>
          
          <div class="section-card">
            <div class="section-header">
              <h3>招聘偏好设置</h3>
              <button class="btn-link" @click="editRecruitmentPrefs = true">编辑</button>
            </div>
            <div class="preferences-container">
              <div v-if="userProfile.recruitmentPreferences" class="preferences-list">
                <div class="pref-item">
                  <div class="pref-label">偏好职位类型</div>
                  <div class="pref-value">{{ userProfile.recruitmentPreferences.positions.join(', ') || '未设置' }}</div>
                </div>
                <div class="pref-item">
                  <div class="pref-label">工作地点</div>
                  <div class="pref-value">{{ userProfile.recruitmentPreferences.locations.join(', ') || '未设置' }}</div>
                </div>
                <div class="pref-item">
                  <div class="pref-label">薪资范围</div>
                  <div class="pref-value">{{ formatSalaryRange(userProfile.recruitmentPreferences.salaryMin, userProfile.recruitmentPreferences.salaryMax) }}</div>
                </div>
                <div class="pref-item">
                  <div class="pref-label">其他要求</div>
                  <div class="pref-value">{{ userProfile.recruitmentPreferences.requirements || '未设置' }}</div>
                </div>
              </div>
              <div v-else class="empty-content">
                <p>您还未设置招聘偏好，设置招聘偏好可以帮助我们推荐更匹配的候选人</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 模式切换确认弹窗 -->
    <div v-if="showModeSwitch" class="modal-overlay">
      <div class="modal-dialog">
        <div class="modal-header">
          <h3>切换用户模式</h3>
          <button class="close-btn" @click="showModeSwitch = false">&times;</button>
        </div>
        <div class="modal-body">
          <p>您确定要从<strong>{{ userMode === 'freelancer' ? '零工用户' : '招聘用户' }}</strong>切换到<strong>{{ userMode === 'freelancer' ? '招聘用户' : '零工用户' }}</strong>模式吗？</p>
          <p>切换后，您将看到不同的界面和功能。您随时可以再次切换回来。</p>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="showModeSwitch = false">取消</button>
          <button 
            class="btn" 
            :class="userMode === 'freelancer' ? 'btn-employer' : 'btn-freelancer'"
            @click="confirmModeSwitch"
          >
            确认切换
          </button>
        </div>
      </div>
    </div>
    
    <!-- 其他可能的编辑弹窗将放在这里 -->
    
    <!-- 基本信息编辑模态框 -->
    <div v-if="editBasicInfo" class="modal-overlay">
      <div class="modal-dialog">
        <div class="modal-header">
          <h3>编辑基本信息</h3>
          <button class="close-btn" @click="editBasicInfo = false">&times;</button>
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
          <button class="btn btn-secondary" @click="cancelEditBasicInfo">取消</button>
          <button class="btn btn-primary" @click="saveBasicInfo">保存</button>
        </div>
      </div>
    </div>
    
    <!-- 个人简介编辑模态框 -->
    <div v-if="editBio" class="modal-overlay">
      <div class="modal-dialog">
        <div class="modal-header">
          <h3>编辑个人简介</h3>
          <button class="close-btn" @click="editBio = false">&times;</button>
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
          <button class="btn btn-secondary" @click="cancelEditBio">取消</button>
          <button class="btn btn-primary" @click="saveBio">保存</button>
        </div>
      </div>
    </div>
    
    <!-- 技能编辑模态框 -->
    <div v-if="editSkills" class="modal-overlay">
      <div class="modal-dialog">
        <div class="modal-header">
          <h3>编辑技能与专长</h3>
          <button class="close-btn" @click="editSkills = false">&times;</button>
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
          <button class="btn btn-secondary" @click="cancelEditSkills">取消</button>
          <button class="btn btn-primary" @click="saveSkills">保存</button>
        </div>
      </div>
    </div>
    
    <!-- 企业信息编辑模态框 -->
    <div v-if="editCompanyInfo" class="modal-overlay">
      <div class="modal-dialog">
        <div class="modal-header">
          <h3>编辑企业信息</h3>
          <button class="close-btn" @click="editCompanyInfo = false">&times;</button>
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
          <button class="btn btn-secondary" @click="cancelEditCompanyInfo">取消</button>
          <button class="btn btn-primary" @click="saveCompanyInfo">保存</button>
        </div>
      </div>
    </div>
    
    <!-- 企业简介编辑模态框 -->
    <div v-if="editCompanyBio" class="modal-overlay">
      <div class="modal-dialog">
        <div class="modal-header">
          <h3>编辑企业简介</h3>
          <button class="close-btn" @click="editCompanyBio = false">&times;</button>
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
          <button class="btn btn-secondary" @click="cancelEditCompanyBio">取消</button>
          <button class="btn btn-primary" @click="saveCompanyBio">保存</button>
        </div>
      </div>
    </div>
    
    <!-- 上传证书模态框 -->
    <div v-if="showCertUpload" class="modal-overlay">
      <div class="modal-dialog">
        <div class="modal-header">
          <h3>上传证书</h3>
          <button class="close-btn" @click="showCertUpload = false">&times;</button>
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
            <label for="cert-issue-date" class="form-label">获得日期</label>
            <input 
              type="date" 
              id="cert-issue-date" 
              class="form-input" 
              v-model="newCertificate.issueDate"
            />
          </div>
          <div class="form-group">
            <label for="cert-file" class="form-label">证书文件</label>
            <div class="file-upload-container">
              <input 
                type="file" 
                id="cert-file" 
                @change="handleCertificateFile" 
                class="file-input"
                accept=".pdf,.jpg,.jpeg,.png"
              />
              <div class="file-upload-btn">
                <span>选择文件</span>
              </div>
              <span class="file-name">{{ newCertificate.file ? newCertificate.file.name : '未选择文件' }}</span>
            </div>
            <p class="form-hint">支持 PDF、JPG、PNG 格式，最大 5MB</p>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="showCertUpload = false">取消</button>
          <button class="btn btn-primary" @click="uploadCertificate" :disabled="!isCertFormValid">上传</button>
        </div>
      </div>
    </div>
    
    <!-- 企业证书上传模态框 -->
    <div v-if="showCompanyCertUpload" class="modal-overlay">
      <div class="modal-dialog">
        <div class="modal-header">
          <h3>上传企业资质</h3>
          <button class="close-btn" @click="showCompanyCertUpload = false">&times;</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label for="company-cert-name" class="form-label">资质证书名称</label>
            <input 
              type="text" 
              id="company-cert-name" 
              class="form-input" 
              v-model="newCompanyCertificate.name" 
              placeholder="请输入资质证书名称"
            />
          </div>
          <div class="form-group">
            <label for="company-cert-issue-date" class="form-label">发证日期</label>
            <input 
              type="date" 
              id="company-cert-issue-date" 
              class="form-input" 
              v-model="newCompanyCertificate.issueDate"
            />
          </div>
          <div class="form-group">
            <label for="company-cert-expiry-date" class="form-label">有效期至</label>
            <input 
              type="date" 
              id="company-cert-expiry-date" 
              class="form-input" 
              v-model="newCompanyCertificate.expiryDate"
            />
          </div>
          <div class="form-group">
            <label for="company-cert-file" class="form-label">证书文件</label>
            <div class="file-upload-container">
              <input 
                type="file" 
                id="company-cert-file" 
                @change="handleCompanyCertificateFile" 
                class="file-input"
                accept=".pdf,.jpg,.jpeg,.png"
              />
              <div class="file-upload-btn">
                <span>选择文件</span>
              </div>
              <span class="file-name">{{ newCompanyCertificate.file ? newCompanyCertificate.file.name : '未选择文件' }}</span>
            </div>
            <p class="form-hint">支持 PDF、JPG、PNG 格式，最大 5MB</p>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="showCompanyCertUpload = false">取消</button>
          <button class="btn btn-primary" @click="uploadCompanyCertificate" :disabled="!isCompanyCertFormValid">上传</button>
        </div>
      </div>
    </div>
    
    <!-- 添加工作经历模态框 -->
    <div v-if="showAddExperience" class="modal-overlay">
      <div class="modal-dialog">
        <div class="modal-header">
          <h3>添加工作经历</h3>
          <button class="close-btn" @click="showAddExperience = false">&times;</button>
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
            <label for="exp-company" class="form-label">公司/组织名称</label>
            <input 
              type="text" 
              id="exp-company" 
              class="form-input" 
              v-model="newExperience.company" 
              placeholder="请输入公司或组织名称"
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
              <input type="checkbox" id="current-job" v-model="isCurrentJob">
              <label for="current-job">目前在职</label>
            </div>
          </div>
          <div class="form-group" v-if="!isCurrentJob">
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
              placeholder="请描述您的职责和成就"
              rows="4"
            ></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="showAddExperience = false">取消</button>
          <button class="btn btn-primary" @click="addExperience" :disabled="!isExperienceFormValid">添加</button>
        </div>
      </div>
    </div>
    
    <!-- 实名认证模态框 -->
    <div v-if="showVerifyForm" class="modal-overlay">
      <div class="modal-dialog">
        <div class="modal-header">
          <h3>实名认证</h3>
          <button class="close-btn" @click="showVerifyForm = false">&times;</button>
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
            <p class="form-hint">您的身份信息将被严格保密，仅用于实名认证</p>
          </div>
          <div class="form-group">
            <label class="form-label">上传身份证照片</label>
            <div class="id-upload-section">
              <div class="id-upload-item">
                <label for="id-front" class="id-upload-label">
                  <div v-if="!verifyForm.idFrontPreview" class="id-upload-placeholder">
                    <i class="upload-icon"></i>
                    <span>上传身份证正面</span>
                  </div>
                  <img v-else :src="verifyForm.idFrontPreview" alt="身份证正面" class="id-preview" />
                </label>
                <input 
                  type="file" 
                  id="id-front" 
                  @change="handleIdFrontUpload" 
                  class="file-input"
                  accept="image/*"
                />
              </div>
              <div class="id-upload-item">
                <label for="id-back" class="id-upload-label">
                  <div v-if="!verifyForm.idBackPreview" class="id-upload-placeholder">
                    <i class="upload-icon"></i>
                    <span>上传身份证背面</span>
                  </div>
                  <img v-else :src="verifyForm.idBackPreview" alt="身份证背面" class="id-preview" />
                </label>
                <input 
                  type="file" 
                  id="id-back" 
                  @change="handleIdBackUpload" 
                  class="file-input"
                  accept="image/*"
                />
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="showVerifyForm = false">取消</button>
          <button class="btn btn-primary" @click="submitVerification" :disabled="!isVerifyFormValid">提交认证</button>
        </div>
      </div>
    </div>
  </BaseLayout>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import BaseLayout from '../../../components/BaseLayout.vue';
import { authStore } from '../../../store/authStore';
import { updateUserProfile } from '../../../services/authService';

// 用户模式 - 'freelancer'(零工用户) 或 'employer'(招聘用户)
const userMode = ref('freelancer');
const showModeSwitch = ref(false);

// 正在编辑的资料副本
const editingProfile = reactive({
  username: '',
  email: '',
  phone: '',
  bio: '',
  skills: []
});

// 正在编辑的公司信息副本
const editingCompany = reactive({
  name: '',
  industry: '',
  address: '',
  size: '',
  description: ''
});

// 新技能临时变量
const newSkill = ref('');

// 获取当前登录用户信息
const currentUser = computed(() => authStore.state.user);

// 模拟的用户资料数据
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
  certificationStatus: '', // 'pending', 'verified', 'failed', 'none'
  skills: [],
  certificates: [],
  experiences: [],
  // 招聘用户特有字段
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

// 编辑状态标记
const editBasicInfo = ref(false);
const editSkills = ref(false);
const editBio = ref(false);
const showCertUpload = ref(false);
const showAddExperience = ref(false);
const showVerifyForm = ref(false);
const editCompanyInfo = ref(false);
const editCompanyBio = ref(false);
const showCompanyCertUpload = ref(false);
const editRecruitmentPrefs = ref(false);

// 新证书表单
const newCertificate = reactive({
  name: '',
  issueDate: '',
  file: null,
  fileUrl: ''
});

// 新企业证书表单
const newCompanyCertificate = reactive({
  name: '',
  issueDate: '',
  expiryDate: '',
  file: null,
  fileUrl: ''
});

// 新工作经历表单
const newExperience = reactive({
  title: '',
  company: '',
  startDate: '',
  endDate: '',
  description: ''
});

// 实名认证表单
const verifyForm = reactive({
  realName: '',
  idNumber: '',
  idFront: null,
  idBack: null,
  idFrontPreview: '',
  idBackPreview: ''
});

// 是否为当前工作标记
const isCurrentJob = ref(false);

// 表单验证计算属性
const isCertFormValid = computed(() => {
  return newCertificate.name && newCertificate.issueDate && newCertificate.file;
});

const isCompanyCertFormValid = computed(() => {
  return newCompanyCertificate.name && newCompanyCertificate.issueDate && newCompanyCertificate.file;
});

const isExperienceFormValid = computed(() => {
  return newExperience.title && newExperience.company && 
         newExperience.startDate && 
         (isCurrentJob.value || newExperience.endDate) && 
         newExperience.description;
});

const isVerifyFormValid = computed(() => {
  return verifyForm.realName && 
         verifyForm.idNumber && 
         verifyForm.idFront && 
         verifyForm.idBack;
});

// 在组件挂载时加载用户资料
onMounted(() => {
  // 如果用户已登录，用当前用户信息初始化资料
  if (currentUser.value) {
    userProfile.username = currentUser.value.username || '';
    userProfile.email = currentUser.value.email || '';
    userProfile.avatar = currentUser.value.avatar || null;
  }
  
  // 在实际项目中，这里会调用API获取完整的用户资料
  // 示例: loadUserProfile();
  
  // 模拟从API加载的数据 - 实际项目中删除这部分
  if (userProfile.username && !userProfile.bio) {
    // 只有在用户名存在但其他资料为空时才加载示例数据
    // 这样实现了"初始注册的用户资料为空"的效果
    loadSampleData();
  }
});

// 加载示例数据 - 实际项目中应替换为API调用
const loadSampleData = () => {
  // 如果不想加载任何示例数据，可以注释掉这个函数调用
  // 或将此函数体留空
};

// 编辑基本信息相关函数
const initEditBasicInfo = () => {
  // 创建资料副本进行编辑
  editingProfile.username = userProfile.username;
  editingProfile.email = userProfile.email;
  editingProfile.phone = userProfile.phone;
  editBasicInfo.value = true;
};

const cancelEditBasicInfo = () => {
  editBasicInfo.value = false;
};

const saveBasicInfo = async () => {
  try {
    // 更新本地状态
    userProfile.username = editingProfile.username;
    userProfile.email = editingProfile.email;
    userProfile.phone = editingProfile.phone;
    
    // 调用API保存到数据库
    await updateProfile({
      username: editingProfile.username,
      email: editingProfile.email,
      phone: editingProfile.phone
    });
    
    editBasicInfo.value = false;
  } catch (error) {
    console.error('保存基本信息失败:', error);
    alert('保存失败，请稍后重试');
  }
};

// 编辑个人简介相关函数
const initEditBio = () => {
  editingProfile.bio = userProfile.bio;
  editBio.value = true;
};

const cancelEditBio = () => {
  editBio.value = false;
};

const saveBio = async () => {
  try {
    // 更新本地状态
    userProfile.bio = editingProfile.bio;
    
    // 调用API保存到数据库
    await updateProfile({
      bio: editingProfile.bio
    });
    
    editBio.value = false;
  } catch (error) {
    console.error('保存个人简介失败:', error);
    alert('保存失败，请稍后重试');
  }
};

// 编辑技能相关函数
const initEditSkills = () => {
  editingProfile.skills = [...userProfile.skills];
  editSkills.value = true;
};

const cancelEditSkills = () => {
  editSkills.value = false;
  newSkill.value = '';
};

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
    // 更新本地状态
    userProfile.skills = [...editingProfile.skills];
    
    // 调用API保存到数据库
    await updateProfile({
      skills: editingProfile.skills
    });
    
    editSkills.value = false;
    newSkill.value = '';
  } catch (error) {
    console.error('保存技能失败:', error);
    alert('保存失败，请稍后重试');
  }
};

// 统一的资料更新函数
const updateProfile = async (profileData) => {
  try {
    // 使用authStore更新当前用户资料
    // 无论是什么类型的资料更新，都通过authStore发送到后端
    await authStore.updateProfile(profileData);
    
    console.log('资料已更新:', profileData);
    return true;
  } catch (error) {
    console.error('更新资料失败:', error);
    throw error;
  }
};

// 工具函数
const getInitials = (name) => {
  if (!name) return '?';
  return name.charAt(0).toUpperCase();
};

const formatDate = (dateStr) => {
  if (!dateStr) return '未设置';
  // 简单格式化，实际项目中可以使用更复杂的日期格式化库
  return dateStr;
};

const formatDateRange = (start, end) => {
  if (!start) return '未设置';
  return `${start} ~ ${end || '至今'}`;
};

const formatSalaryRange = (min, max) => {
  if (!min && !max) return '未设置';
  if (!max) return `${min}元/月以上`;
  if (!min) return `${max}元/月以下`;
  return `${min} - ${max}元/月`;
};

const maskPhone = (phone) => {
  if (!phone) return '未设置';
  return phone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2');
};

const maskEmail = (email) => {
  if (!email) return '未设置';
  const parts = email.split('@');
  if (parts.length !== 2) return email;
  const name = parts[0];
  const maskedName = name.length > 3 
    ? name.substring(0, 2) + '*'.repeat(name.length - 3) + name.substring(name.length - 1)
    : name.substring(0, 1) + '*'.repeat(name.length - 1);
  return maskedName + '@' + parts[1];
};

const maskRealName = (name) => {
  if (!name) return '未设置';
  if (name.length <= 2) return name.substring(0, 1) + '*';
  return name.substring(0, 1) + '*'.repeat(name.length - 2) + name.substring(name.length - 1);
};

// 信誉分相关
const getCreditScoreClass = (score) => {
  if (!score) return 'score-unknown';
  if (score >= 90) return 'score-excellent';
  if (score >= 80) return 'score-good';
  if (score >= 60) return 'score-average';
  return 'score-poor';
};

// 认证状态相关
const getCertificationClass = (status) => {
  switch (status) {
    case 'verified': return 'verified';
    case 'pending': return 'pending';
    case 'failed': return 'failed';
    default: return 'unverified';
  }
};

const getCertificationText = (status) => {
  switch (status) {
    case 'verified': return '已认证';
    case 'pending': return '认证中';
    case 'failed': return '认证失败';
    default: return '未认证';
  }
};

// 证书状态相关
const getCertStatusClass = (status) => {
  switch (status) {
    case 'verified': return 'status-verified';
    case 'pending': return 'status-pending';
    case 'rejected': return 'status-rejected';
    default: return 'status-unknown';
  }
};

const getCertStatusText = (status) => {
  switch (status) {
    case 'verified': return '已验证';
    case 'pending': return '审核中';
    case 'rejected': return '已拒绝';
    default: return '未知状态';
  }
};

// 企业验证状态相关
const getCompanyVerifyClass = (status) => {
  switch (status) {
    case 'verified': return 'company-verified';
    case 'pending': return 'company-pending';
    case 'rejected': return 'company-rejected';
    default: return 'company-unverified';
  }
};

const getCompanyVerifyText = (status) => {
  switch (status) {
    case 'verified': return '企业已认证';
    case 'pending': return '企业认证中';
    case 'rejected': return '企业认证未通过';
    default: return '企业未认证';
  }
};

// 处理模式切换
const handleModeSwitch = () => {
  showModeSwitch.value = true;
};

const confirmModeSwitch = () => {
  userMode.value = userMode.value === 'freelancer' ? 'employer' : 'freelancer';
  showModeSwitch.value = false;
};

// 头像上传处理
const handleAvatarChange = (event) => {
  const file = event.target.files[0];
  if (!file) return;
  
  // 实际项目中应该上传到服务器，这里只是模拟
  const reader = new FileReader();
  reader.onload = (e) => {
    userProfile.avatar = e.target.result;
  };
  reader.readAsDataURL(file);
};

// 查看证书相关
const viewCertificate = (cert) => {
  // 实际项目中应该打开证书详情或预览
  console.log('查看证书:', cert);
  alert(`查看证书: ${cert.name}`);
};

const viewCompanyCertificate = (cert) => {
  // 实际项目中应该打开证书详情或预览
  console.log('查看企业证书:', cert);
  alert(`查看企业证书: ${cert.name}`);
};

// 编辑企业信息相关函数
const initEditCompanyInfo = () => {
  editingCompany.name = userProfile.company?.name || '';
  editingCompany.industry = userProfile.company?.industry || '';
  editingCompany.address = userProfile.company?.address || '';
  editingCompany.size = userProfile.company?.size || '';
  editCompanyInfo.value = true;
};

const cancelEditCompanyInfo = () => {
  editCompanyInfo.value = false;
};

const saveCompanyInfo = async () => {
  try {
    // 确保company对象存在
    if (!userProfile.company) {
      userProfile.company = {
        name: '',
        logo: null,
        verifyStatus: '',
        industry: '',
        address: '',
        size: '',
        description: '',
        certificates: []
      };
    }
    
    // 更新本地状态
    userProfile.company.name = editingCompany.name;
    userProfile.company.industry = editingCompany.industry;
    userProfile.company.address = editingCompany.address;
    userProfile.company.size = editingCompany.size;
    
    // 调用API保存到数据库
    await updateProfile({
      company: {
        name: editingCompany.name,
        industry: editingCompany.industry,
        address: editingCompany.address,
        size: editingCompany.size
      }
    });
    
    editCompanyInfo.value = false;
  } catch (error) {
    console.error('保存企业信息失败:', error);
    alert('保存失败，请稍后重试');
  }
};

// 编辑企业简介相关函数
const initEditCompanyBio = () => {
  editingCompany.description = userProfile.company?.description || '';
  editCompanyBio.value = true;
};

const cancelEditCompanyBio = () => {
  editCompanyBio.value = false;
};

const saveCompanyBio = async () => {
  try {
    // 确保company对象存在
    if (!userProfile.company) {
      userProfile.company = {
        name: '',
        logo: null,
        verifyStatus: '',
        industry: '',
        address: '',
        size: '',
        description: '',
        certificates: []
      };
    }
    
    // 更新本地状态
    userProfile.company.description = editingCompany.description;
    
    // 调用API保存到数据库
    await updateProfile({
      company: {
        description: editingCompany.description
      }
    });
    
    editCompanyBio.value = false;
  } catch (error) {
    console.error('保存企业简介失败:', error);
    alert('保存失败，请稍后重试');
  }
};

// 处理证书文件选择
const handleCertificateFile = (event) => {
  const file = event.target.files[0];
  if (!file) return;
  
  // 检查文件大小
  if (file.size > 5 * 1024 * 1024) {
    alert('文件大小不能超过5MB');
    return;
  }
  
  // 检查文件类型
  const fileTypes = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png'];
  if (!fileTypes.includes(file.type)) {
    alert('只支持PDF、JPG、PNG格式文件');
    return;
  }
  
  newCertificate.file = file;
  
  // 如果是图片，生成预览
  if (file.type.startsWith('image/')) {
    const reader = new FileReader();
    reader.onload = (e) => {
      newCertificate.fileUrl = e.target.result;
    };
    reader.readAsDataURL(file);
  }
};

// 处理企业证书文件选择
const handleCompanyCertificateFile = (event) => {
  const file = event.target.files[0];
  if (!file) return;
  
  // 检查文件大小
  if (file.size > 5 * 1024 * 1024) {
    alert('文件大小不能超过5MB');
    return;
  }
  
  // 检查文件类型
  const fileTypes = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png'];
  if (!fileTypes.includes(file.type)) {
    alert('只支持PDF、JPG、PNG格式文件');
    return;
  }
  
  newCompanyCertificate.file = file;
  
  // 如果是图片，生成预览
  if (file.type.startsWith('image/')) {
    const reader = new FileReader();
    reader.onload = (e) => {
      newCompanyCertificate.fileUrl = e.target.result;
    };
    reader.readAsDataURL(file);
  }
};

// 上传证书
const uploadCertificate = async () => {
  try {
    // 在实际项目中，这里会使用FormData上传文件到后端
    // 模拟上传成功
    const newCert = {
      id: Date.now().toString(), // 模拟ID
      name: newCertificate.name,
      issueDate: newCertificate.issueDate,
      verifyStatus: 'pending', // 新上传的证书默认状态为"审核中"
      fileUrl: newCertificate.fileUrl || 'https://example.com/certificate.pdf' // 模拟文件URL
    };
    
    // 确保certificates数组存在
    if (!userProfile.certificates) {
      userProfile.certificates = [];
    }
    
    // 添加到本地状态
    userProfile.certificates.push(newCert);
    
    // 清空表单
    newCertificate.name = '';
    newCertificate.issueDate = '';
    newCertificate.file = null;
    newCertificate.fileUrl = '';
    
    showCertUpload.value = false;
    
    // 提示用户
    alert('证书上传成功，等待审核');
  } catch (error) {
    console.error('上传证书失败:', error);
    alert('上传失败，请稍后重试');
  }
};

// 上传企业证书
const uploadCompanyCertificate = async () => {
  try {
    // 在实际项目中，这里会使用FormData上传文件到后端
    // 模拟上传成功
    const newCert = {
      id: Date.now().toString(), // 模拟ID
      name: newCompanyCertificate.name,
      issueDate: newCompanyCertificate.issueDate,
      expiryDate: newCompanyCertificate.expiryDate,
      verifyStatus: 'pending', // 新上传的证书默认状态为"审核中"
      fileUrl: newCompanyCertificate.fileUrl || 'https://example.com/company-certificate.pdf' // 模拟文件URL
    };
    
    // 确保company和certificates数组存在
    if (!userProfile.company) {
      userProfile.company = {
        name: '',
        logo: null,
        verifyStatus: '',
        industry: '',
        address: '',
        size: '',
        description: '',
        certificates: []
      };
    }
    
    if (!userProfile.company.certificates) {
      userProfile.company.certificates = [];
    }
    
    // 添加到本地状态
    userProfile.company.certificates.push(newCert);
    
    // 清空表单
    newCompanyCertificate.name = '';
    newCompanyCertificate.issueDate = '';
    newCompanyCertificate.expiryDate = '';
    newCompanyCertificate.file = null;
    newCompanyCertificate.fileUrl = '';
    
    showCompanyCertUpload.value = false;
    
    // 提示用户
    alert('企业资质上传成功，等待审核');
  } catch (error) {
    console.error('上传企业资质失败:', error);
    alert('上传失败，请稍后重试');
  }
};

// 添加工作经历
const addExperience = async () => {
  try {
    // 构建工作经历对象
    const experience = {
      id: Date.now().toString(), // 模拟ID
      title: newExperience.title,
      company: newExperience.company,
      startDate: newExperience.startDate,
      endDate: isCurrentJob.value ? null : newExperience.endDate,
      description: newExperience.description
    };
    
    // 确保experiences数组存在
    if (!userProfile.experiences) {
      userProfile.experiences = [];
    }
    
    // 添加到本地状态
    userProfile.experiences.push(experience);
    
    // 重置表单
    newExperience.title = '';
    newExperience.company = '';
    newExperience.startDate = '';
    newExperience.endDate = '';
    newExperience.description = '';
    isCurrentJob.value = false;
    
    showAddExperience.value = false;
    
    // 提示用户
    alert('工作经历添加成功');
    
    // 在实际项目中，这里会调用API保存到数据库
    await updateProfile({
      experiences: userProfile.experiences
    });
  } catch (error) {
    console.error('添加工作经历失败:', error);
    alert('添加失败，请稍后重试');
  }
};

// 处理身份证正面上传
const handleIdFrontUpload = (event) => {
  const file = event.target.files[0];
  if (!file) return;
  
  // 检查文件大小
  if (file.size > 5 * 1024 * 1024) {
    alert('文件大小不能超过5MB');
    return;
  }
  
  // 检查文件类型
  if (!file.type.startsWith('image/')) {
    alert('请上传图片格式的身份证照片');
    return;
  }
  
  verifyForm.idFront = file;
  
  // 生成预览
  const reader = new FileReader();
  reader.onload = (e) => {
    verifyForm.idFrontPreview = e.target.result;
  };
  reader.readAsDataURL(file);
};

// 处理身份证背面上传
const handleIdBackUpload = (event) => {
  const file = event.target.files[0];
  if (!file) return;
  
  // 检查文件大小
  if (file.size > 5 * 1024 * 1024) {
    alert('文件大小不能超过5MB');
    return;
  }
  
  // 检查文件类型
  if (!file.type.startsWith('image/')) {
    alert('请上传图片格式的身份证照片');
    return;
  }
  
  verifyForm.idBack = file;
  
  // 生成预览
  const reader = new FileReader();
  reader.onload = (e) => {
    verifyForm.idBackPreview = e.target.result;
  };
  reader.readAsDataURL(file);
};

// 提交实名认证
const submitVerification = async () => {
  try {
    // 身份证号码简单验证
    const idRegex = /(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)/;
    if (!idRegex.test(verifyForm.idNumber)) {
      alert('请输入有效的身份证号码');
      return;
    }
    
    // 在实际项目中，这里会使用FormData上传身份证照片到后端
    // 模拟实名认证提交成功
    
    // 更新本地状态 - 修改为提交后为"审核中"状态，而不是直接认证通过
    userProfile.realNameStatus = 'pending'; // 'pending', 'verified', 'failed'
    userProfile.realName = verifyForm.realName;
    userProfile.verifySubmitTime = new Date().toISOString().split('T')[0]; // 当前日期
    
    // 重置表单
    verifyForm.realName = '';
    verifyForm.idNumber = '';
    verifyForm.idFront = null;
    verifyForm.idBack = null;
    verifyForm.idFrontPreview = '';
    verifyForm.idBackPreview = '';
    
    showVerifyForm.value = false;
    
    // 提示用户
    alert('实名认证信息提交成功，等待审核');
    
    // 在实际项目中，这里会调用API保存到数据库
    await updateProfile({
      realNameStatus: 'pending',
      realName: userProfile.realName,
      verifySubmitTime: userProfile.verifySubmitTime
    });
  } catch (error) {
    console.error('提交实名认证失败:', error);
    alert('提交失败，请稍后重试');
  }
};
</script>

<style scoped>
/* 主要颜色设置 - 零工蓝色和雇主橙色 */
:root {
  --freelancer-color: #3498db;
  --freelancer-light: #e1f0fa;
  --freelancer-dark: #2980b9;
  --employer-color: #e67e22;
  --employer-light: #fae5d3;
  --employer-dark: #d35400;
}

.profile-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 1rem;
}

/* 用户模式切换 */
.user-mode-switch {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: var(--freelancer-light);
  padding: 1rem;
  border-radius: var(--border-radius);
  margin-bottom: 1.5rem;
  transition: background-color 0.3s ease;
}

.user-mode-switch.employer-mode {
  background-color: var(--employer-light);
}

.current-mode {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 500;
}

.mode-color {
  display: inline-block;
  width: 1rem;
  height: 1rem;
  border-radius: 50%;
}

.mode-color.freelancer {
  background-color: var(--freelancer-color);
}

.mode-color.employer {
  background-color: var(--employer-color);
}

.mode-switch-btn {
  padding: 0.5rem 1rem;
  border-radius: var(--border-radius);
  font-weight: 500;
}

.btn-freelancer {
  background-color: var(--freelancer-color);
  color: white;
}

.btn-freelancer:hover {
  background-color: var(--freelancer-dark);
}

.btn-employer {
  background-color: var(--employer-color);
  color: white;
}

.btn-employer:hover {
  background-color: var(--employer-dark);
}

/* 个人资料卡片 */
.profile-card {
  background-color: var(--white);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow);
  overflow: hidden;
}

.profile-header {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  padding: 2rem;
  border-bottom: 1px solid var(--border-color);
  background-color: var(--background-color);
}

@media (max-width: 768px) {
  .profile-header {
    flex-direction: column;
  }
}

.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.avatar-container {
  position: relative;
  width: 120px;
  height: 120px;
}

.avatar {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid var(--primary-color);
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background-color: var(--primary-color);
  color: var(--accent-color);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 48px;
  font-weight: bold;
}

.avatar-upload {
  position: absolute;
  right: 0;
  bottom: 0;
}

.avatar-edit-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background-color: var(--white);
  border-radius: 50%;
  box-shadow: var(--shadow);
  cursor: pointer;
}

.edit-icon {
  display: inline-block;
  width: 16px;
  height: 16px;
  background-color: var(--accent-color);
  /* 实际项目中应该使用真实图标 */
}

.hidden {
  display: none;
}

.credit-score {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0.5rem;
  border-radius: var(--border-radius);
  background-color: white;
  box-shadow: var(--shadow-sm);
}

.score-value {
  font-size: 1.5rem;
  font-weight: bold;
}

.score-label {
  font-size: 0.8rem;
  color: var(--text-light);
}

.score-excellent {
  color: #27ae60;
}

.score-good {
  color: #2ecc71;
}

.score-average {
  color: #f39c12;
}

.score-poor {
  color: #e74c3c;
}

.score-unknown {
  color: var(--text-light);
}

.user-basic-info {
  flex: 1;
}

.username {
  margin-bottom: 0.5rem;
}

.verify-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.badge {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem 0.5rem;
  border-radius: 1rem;
  font-size: 0.8rem;
}

.badge.verified {
  background-color: rgba(39, 174, 96, 0.1);
  color: #27ae60;
}

.badge.unverified {
  background-color: rgba(189, 195, 199, 0.1);
  color: #7f8c8d;
}

.badge.pending {
  background-color: rgba(243, 156, 18, 0.1);
  color: #f39c12;
}

.badge.failed {
  background-color: rgba(231, 76, 60, 0.1);
  color: #e74c3c;
}

.contact-info {
  margin-top: 1rem;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  color: var(--text-light);
}

.icon {
  display: inline-block;
  width: 16px;
  height: 16px;
  background-color: var(--text-light);
  /* 实际项目中应该使用真实图标 */
}

.profile-actions {
  display: flex;
  align-items: flex-start;
}

/* 内容部分共享样式 */
.section-card {
  padding: 1.5rem;
  border-bottom: 1px solid var(--border-color);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.section-header h3 {
  margin: 0;
  font-size: 1.2rem;
  color: var(--accent-color);
}

.btn-link {
  background: none;
  border: none;
  color: var(--secondary-color);
  cursor: pointer;
  padding: 0;
  font-size: 0.9rem;
}

.btn-link:hover {
  text-decoration: underline;
}

.empty-content {
  background-color: var(--background-color);
  padding: 1rem;
  border-radius: var(--border-radius);
  color: var(--text-light);
  text-align: center;
}

/* 零工模式样式 */
.skills-container {
  margin-bottom: 1rem;
}

.skills-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.skill-tag {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  background-color: var(--primary-light);
  color: var(--accent-color);
  border-radius: 1rem;
  font-size: 0.9rem;
}

.bio-container {
  line-height: 1.6;
}

.certificates-container, .experience-container {
  margin-top: 1rem;
}

.cert-list, .experience-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.cert-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background-color: var(--background-color);
  border-radius: var(--border-radius);
}

.cert-name {
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.cert-date {
  font-size: 0.85rem;
  color: var(--text-light);
  margin-bottom: 0.25rem;
}

.cert-status {
  font-size: 0.85rem;
}

.status-verified {
  color: #27ae60;
}

.status-pending {
  color: #f39c12;
}

.status-rejected {
  color: #e74c3c;
}

.exp-item {
  display: flex;
  gap: 1rem;
  padding: 0.5rem 0;
}

.exp-timeline {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 120px;
}

.exp-duration {
  font-size: 0.85rem;
  color: var(--text-light);
  margin-bottom: 0.5rem;
  white-space: nowrap;
}

.exp-duration-line {
  flex: 1;
  width: 2px;
  background-color: var(--border-color);
}

.exp-content {
  flex: 1;
}

.exp-title {
  font-weight: 500;
  margin-bottom: 0.5rem;
}

.exp-description {
  font-size: 0.95rem;
  line-height: 1.5;
}

.verify-info {
  background-color: var(--background-color);
  padding: 1rem;
  border-radius: var(--border-radius);
}

.verify-success {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #27ae60;
  margin-bottom: 0.5rem;
}

.icon-success {
  display: inline-block;
  width: 16px;
  height: 16px;
  background-color: #27ae60;
  border-radius: 50%;
  /* 实际项目中应该使用真实图标 */
}

.verify-detail {
  font-size: 0.9rem;
  color: var(--text-color);
}

.verify-detail p {
  margin: 0.25rem 0;
}

/* 招聘模式样式 */
.company-container {
  margin-bottom: 1rem;
}

.company-info {
  display: flex;
  gap: 1.5rem;
}

@media (max-width: 768px) {
  .company-info {
    flex-direction: column;
    align-items: center;
  }
}

.company-logo-container {
  min-width: 100px;
}

.company-logo {
  width: 100px;
  height: 100px;
  border-radius: var(--border-radius);
  object-fit: cover;
}

.company-logo-placeholder {
  width: 100px;
  height: 100px;
  border-radius: var(--border-radius);
  background-color: var(--employer-light);
  color: var(--employer-dark);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: bold;
}

.company-details {
  flex: 1;
}

.company-name {
  margin-top: 0;
  margin-bottom: 0.5rem;
}

.company-verify-status {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 1rem;
  font-size: 0.8rem;
  margin-bottom: 1rem;
}

.company-verified {
  background-color: rgba(39, 174, 96, 0.1);
  color: #27ae60;
}

.company-pending {
  background-color: rgba(243, 156, 18, 0.1);
  color: #f39c12;
}

.company-rejected {
  background-color: rgba(231, 76, 60, 0.1);
  color: #e74c3c;
}

.company-unverified {
  background-color: rgba(189, 195, 199, 0.1);
  color: #7f8c8d;
}

.company-info-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.company-info-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--text-light);
  font-size: 0.95rem;
}

.company-bio-container {
  line-height: 1.6;
}

.preferences-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
}

.pref-item {
  padding: 1rem;
  background-color: var(--background-color);
  border-radius: var(--border-radius);
}

.pref-label {
  font-weight: 500;
  margin-bottom: 0.5rem;
  color: var(--accent-color);
}

.pref-value {
  color: var(--text-color);
}

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

/* 文件上传样式 */
.file-upload-container {
  position: relative;
  display: flex;
  align-items: center;
}

.file-input {
  position: absolute;
  width: 0.1px;
  height: 0.1px;
  opacity: 0;
  overflow: hidden;
  z-index: -1;
}

.file-upload-btn {
  display: inline-block;
  padding: 0.6rem 1.2rem;
  background-color: var(--background-color);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  cursor: pointer;
  white-space: nowrap;
}

.file-upload-btn:hover {
  background-color: var(--primary-light);
}

.file-name {
  margin-left: 1rem;
  font-size: 0.9rem;
  color: var(--text-light);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 200px;
}

/* 身份证上传样式 */
.id-upload-section {
  display: flex;
  gap: 1rem;
}

.id-upload-item {
  flex: 1;
}

.id-upload-label {
  display: block;
  width: 100%;
  height: 150px;
  border: 2px dashed var(--border-color);
  border-radius: var(--border-radius);
  cursor: pointer;
  overflow: hidden;
}

.id-upload-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: var(--text-light);
}

.upload-icon {
  display: inline-block;
  width: 32px;
  height: 32px;
  margin-bottom: 0.5rem;
  background-color: var(--text-light);
  /* 实际项目中应该使用真实图标 */
}

.id-preview {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.form-checkbox {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* 实名认证状态样式 */
.verify-pending .verify-status-pending {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #f39c12;
  margin-bottom: 0.5rem;
}

.verify-failed .verify-status-failed {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #e74c3c;
  margin-bottom: 0.5rem;
}

.icon-pending {
  display: inline-block;
  width: 16px;
  height: 16px;
  background-color: #f39c12;
  border-radius: 50%;
  /* 实际项目中应该使用真实图标 */
}

.icon-failed {
  display: inline-block;
  width: 16px;
  height: 16px;
  background-color: #e74c3c;
  border-radius: 50%;
  /* 实际项目中应该使用真实图标 */
}

.verify-note {
  font-style: italic;
  color: var(--text-light);
  margin-top: 0.5rem;
}
</style>
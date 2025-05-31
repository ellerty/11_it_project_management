import httpService from './httpService';

class ResumeService {
  async uploadResume(file: File) {
    const formData = new FormData();
    formData.append('pdf_file', file);

    try {
      const response = await httpService.post('/auth/resume/upload/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response;
    } catch (error: any) {
      console.error('上传简历失败:', error);
      if (error.response?.data?.error) {
        throw new Error(error.response.data.error);
      }
      throw error;
    }
  }

  async getResume() {
    try {
      const response = await httpService.get('/auth/resume/upload/');
      return response;
    } catch (error: any) {
      console.error('获取简历失败:', error);
      if (error.response?.data?.error) {
        throw new Error(error.response.data.error);
      }
      throw error;
    }
  }
}

export default new ResumeService();

// سرویس مدیریت دروس - متصل به API واقعی
import { apiRequest } from '../api.js'

// تبدیل خطاهای API به پیام‌های فارسی
function handleApiError(error, defaultMessage) {
  if (error.message) {
    return error.message
  }
  if (error.detail) {
    return error.detail
  }
  if (typeof error === 'string') {
    return error
  }
  return defaultMessage || 'خطایی رخ داد'
}

export async function getCourses() {
  try {
    const response = await apiRequest('/courses/')
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || 'خطا در دریافت لیست دروس')
    }
    
    return await response.json()
  } catch (error) {
    console.error('Error fetching courses:', error)
    throw new Error(handleApiError(error, 'خطا در دریافت لیست دروس'))
  }
}

export async function getCourse(id) {
  try {
    const response = await apiRequest(`/courses/${id}/`)
    
    if (!response.ok) {
      if (response.status === 404) {
        throw new Error('درس یافت نشد')
      }
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || 'خطا در دریافت جزئیات درس')
    }
    
    return await response.json()
  } catch (error) {
    console.error('Error fetching course:', error)
    throw new Error(handleApiError(error, 'خطا در دریافت جزئیات درس'))
  }
}

export async function createCourse(courseData) {
  try {
    const response = await apiRequest('/courses/', {
      method: 'POST',
      body: JSON.stringify(courseData),
    })
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      
      // مدیریت خطاهای اعتبارسنجی
      if (response.status === 400) {
        const errorMessages = []
        if (errorData.code) {
          errorMessages.push(...(Array.isArray(errorData.code) ? errorData.code : [errorData.code]))
        }
        if (errorData.name) {
          errorMessages.push(...(Array.isArray(errorData.name) ? errorData.name : [errorData.name]))
        }
        if (errorData.non_field_errors) {
          errorMessages.push(...(Array.isArray(errorData.non_field_errors) ? errorData.non_field_errors : [errorData.non_field_errors]))
        }
        throw new Error(errorMessages.length > 0 ? errorMessages.join(', ') : 'اطلاعات وارد شده معتبر نیست')
      }
      
      if (response.status === 403) {
        throw new Error('شما دسترسی لازم برای این عملیات را ندارید')
      }
      
      throw new Error(errorData.detail || 'خطا در ایجاد درس')
    }
    
    return await response.json()
  } catch (error) {
    console.error('Error creating course:', error)
    throw new Error(handleApiError(error, 'خطا در ایجاد درس'))
  }
}

export async function updateCourse(id, courseData) {
  try {
    const response = await apiRequest(`/courses/${id}/`, {
      method: 'PUT',
      body: JSON.stringify(courseData),
    })
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      
      // مدیریت خطاهای اعتبارسنجی
      if (response.status === 400) {
        const errorMessages = []
        if (errorData.code) {
          errorMessages.push(...(Array.isArray(errorData.code) ? errorData.code : [errorData.code]))
        }
        if (errorData.name) {
          errorMessages.push(...(Array.isArray(errorData.name) ? errorData.name : [errorData.name]))
        }
        if (errorData.non_field_errors) {
          errorMessages.push(...(Array.isArray(errorData.non_field_errors) ? errorData.non_field_errors : [errorData.non_field_errors]))
        }
        throw new Error(errorMessages.length > 0 ? errorMessages.join(', ') : 'اطلاعات وارد شده معتبر نیست')
      }
      
      if (response.status === 403) {
        throw new Error('شما دسترسی لازم برای این عملیات را ندارید')
      }
      
      if (response.status === 404) {
        throw new Error('درس یافت نشد')
      }
      
      throw new Error(errorData.detail || 'خطا در به‌روزرسانی درس')
    }
    
    return await response.json()
  } catch (error) {
    console.error('Error updating course:', error)
    throw new Error(handleApiError(error, 'خطا در به‌روزرسانی درس'))
  }
}

export async function deleteCourse(id) {
  try {
    const response = await apiRequest(`/courses/${id}/`, {
      method: 'DELETE',
    })
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      
      if (response.status === 403) {
        throw new Error('شما دسترسی لازم برای این عملیات را ندارید')
      }
      
      if (response.status === 404) {
        throw new Error('درس یافت نشد')
      }
      
      throw new Error(errorData.detail || 'خطا در حذف درس')
    }
    
    // DELETE ممکن است body نداشته باشد
    if (response.status === 204) {
      return { success: true }
    }
    
    return await response.json().catch(() => ({ success: true }))
  } catch (error) {
    console.error('Error deleting course:', error)
    throw new Error(handleApiError(error, 'خطا در حذف درس'))
  }
}


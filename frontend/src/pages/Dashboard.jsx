import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import CourseModal from '../components/CourseModal'
import ConfirmDialog from '../components/ConfirmDialog'
import ToastContainer from '../components/ToastContainer'
import { useToast } from '../hooks/useToast'
import { getCourses, createCourse, updateCourse, deleteCourse } from '../services/courseService'

function Dashboard() {
  const [courses, setCourses] = useState([])
  const [loading, setLoading] = useState(true)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [editingCourse, setEditingCourse] = useState(null)
  const [deleteConfirm, setDeleteConfirm] = useState(null)
  const { logout } = useAuth()
  const navigate = useNavigate()
  const { toasts, success, error, removeToast } = useToast()

  useEffect(() => {
    loadCourses()
  }, [])

  const loadCourses = async () => {
    setLoading(true)
    try {
      const data = await getCourses()
      setCourses(data)
    } catch (err) {
      console.error('خطا در بارگذاری دروس:', err)
      error(err.message || 'خطا در بارگذاری دروس')
    } finally {
      setLoading(false)
    }
  }

  const handleAddCourse = () => {
    setEditingCourse(null)
    setIsModalOpen(true)
  }

  const handleEditCourse = (course) => {
    setEditingCourse(course)
    setIsModalOpen(true)
  }

  const handleDeleteClick = (course) => {
    setDeleteConfirm(course)
  }

  const handleDeleteConfirm = async () => {
    if (!deleteConfirm) return

    try {
      await deleteCourse(deleteConfirm.id)
      success(`درس "${deleteConfirm.name}" با موفقیت حذف شد`)
      setDeleteConfirm(null)
      await loadCourses()
    } catch (err) {
      error(err.message || 'خطا در حذف درس')
      setDeleteConfirm(null)
    }
  }

  const handleModalClose = () => {
    setIsModalOpen(false)
    setEditingCourse(null)
  }

  const handleModalSave = async (courseData) => {
    try {
      if (editingCourse) {
        await updateCourse(editingCourse.id, courseData)
        success(`درس "${courseData.name}" با موفقیت به‌روزرسانی شد`)
      } else {
        await createCourse(courseData)
        success(`درس "${courseData.name}" با موفقیت اضافه شد`)
      }
      await loadCourses()
      handleModalClose()
    } catch (err) {
      error(err.message || 'خطا در ذخیره درس')
    }
  }

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const days = ['شنبه', 'یکشنبه', 'دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنج‌شنبه', 'جمعه']

  return (
    <div className="min-h-screen bg-gray-50">
      <ToastContainer toasts={toasts} onRemove={removeToast} />
      
      {/* Header - Fixed */}
      <header className="sticky top-0 z-40 bg-white shadow-xl border-b-2 border-blue-100 backdrop-blur-sm bg-opacity-95">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-5">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-4">
              <div className="flex items-center justify-center w-14 h-14 bg-gradient-to-br from-blue-600 via-blue-500 to-indigo-600 rounded-2xl shadow-lg transform hover:scale-105 transition-transform duration-300">
                <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
              </div>
              <div>
                <h1 className="text-3xl font-extrabold bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 bg-clip-text text-transparent">
                  داشبورد مدیر
                </h1>
                <p className="text-sm text-gray-600 mt-1 font-medium">مدیریت و ویرایش دروس دانشگاه</p>
              </div>
            </div>
            <button
              onClick={handleLogout}
              className="btn-secondary flex items-center gap-2 font-semibold"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
              <span>خروج</span>
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats and Add Course Button */}
        <div className="mb-8 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-6">
          <div className="flex items-center gap-4">
            <div className="bg-white rounded-2xl shadow-xl px-6 py-4 border-2 border-blue-100 hover:shadow-2xl transition-all duration-300">
              <div className="text-sm font-semibold text-gray-600 mb-1">تعداد دروس</div>
              <div className="text-3xl font-extrabold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                {courses.length}
              </div>
            </div>
          </div>
          <button
            onClick={handleAddCourse}
            className="btn-primary flex items-center gap-3 text-lg px-8 py-4 shadow-2xl"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M12 4v16m8-8H4" />
            </svg>
            <span className="font-bold">افزودن درس جدید</span>
          </button>
        </div>

        {/* Courses Table */}
        <div className="card overflow-hidden p-0 border-2 border-blue-100 shadow-2xl">
          {loading ? (
            <div className="text-center py-20">
              <div className="inline-block spinner w-12 h-12 border-4 border-blue-600 border-r-transparent"></div>
              <p className="mt-6 text-gray-600 font-semibold text-lg">در حال بارگذاری...</p>
            </div>
          ) : courses.length === 0 ? (
            <div className="text-center py-20">
              <div className="inline-flex items-center justify-center w-24 h-24 bg-gradient-to-br from-blue-100 to-indigo-100 rounded-full mb-6 shadow-lg">
                <svg className="w-12 h-12 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
              </div>
              <p className="text-xl font-bold text-gray-800 mb-2">هنوز درسی اضافه نشده است</p>
              <p className="text-sm text-gray-500 mb-8">برای شروع، اولین درس را اضافه کنید</p>
              <button
                onClick={handleAddCourse}
                className="btn-primary text-lg px-8 py-4"
              >
                افزودن اولین درس
              </button>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead>
                  <tr>
                    <th className="table-header">کد درس</th>
                    <th className="table-header">نام درس</th>
                    <th className="table-header">استاد</th>
                    <th className="table-header">روز</th>
                    <th className="table-header">ساعت</th>
                    <th className="table-header">مکان</th>
                    <th className="table-header">ظرفیت</th>
                    <th className="table-header">واحد</th>
                    <th className="table-header">عملیات</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {courses.map((course, index) => (
                    <tr 
                      key={course.id} 
                      className="hover:bg-gradient-to-r hover:from-blue-50 hover:via-indigo-50 hover:to-purple-50 transition-all duration-300 border-b border-gray-100 hover:border-blue-200 hover:shadow-md"
                    >
                      <td className="table-cell font-semibold text-gray-900">
                        <span className="badge-primary">{course.code}</span>
                      </td>
                      <td className="table-cell font-medium text-gray-900">
                        {course.name}
                      </td>
                      <td className="table-cell text-gray-600">
                        {course.professor || <span className="text-gray-400">-</span>}
                      </td>
                      <td className="table-cell text-gray-600">
                        {course.day || <span className="text-gray-400">-</span>}
                      </td>
                      <td className="table-cell text-gray-600">
                        {course.time || <span className="text-gray-400">-</span>}
                      </td>
                      <td className="table-cell text-gray-600">
                        {course.location || <span className="text-gray-400">-</span>}
                      </td>
                      <td className="table-cell">
                        <span className="badge badge-warning">{course.capacity}</span>
                      </td>
                      <td className="table-cell">
                        <span className="badge badge-success">{course.units} واحد</span>
                      </td>
                      <td className="table-cell">
                        <div className="flex gap-3">
                          <button
                            onClick={() => handleEditCourse(course)}
                            className="p-2.5 rounded-xl bg-blue-50 hover:bg-blue-100 text-blue-600 hover:text-blue-700 transition-all duration-200 shadow-sm hover:shadow-md transform hover:scale-110"
                            title="ویرایش"
                          >
                            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                            </svg>
                          </button>
                          <button
                            onClick={() => handleDeleteClick(course)}
                            className="p-2.5 rounded-xl bg-red-50 hover:bg-red-100 text-red-600 hover:text-red-700 transition-all duration-200 shadow-sm hover:shadow-md transform hover:scale-110"
                            title="حذف"
                          >
                            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                            </svg>
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </main>

      {/* Course Modal */}
      {isModalOpen && (
        <CourseModal
          course={editingCourse}
          onClose={handleModalClose}
          onSave={handleModalSave}
        />
      )}

      {/* Delete Confirmation Dialog */}
      <ConfirmDialog
        isOpen={!!deleteConfirm}
        title="حذف درس"
        message={`آیا از حذف درس "${deleteConfirm?.name}" اطمینان دارید؟ این عمل قابل بازگشت نیست.`}
        onConfirm={handleDeleteConfirm}
        onCancel={() => setDeleteConfirm(null)}
        confirmText="حذف"
        cancelText="انصراف"
        type="danger"
      />
    </div>
  )
}

export default Dashboard


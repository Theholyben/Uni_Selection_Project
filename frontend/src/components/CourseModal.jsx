import { useState, useEffect } from 'react'

function CourseModal({ course, onClose, onSave }) {
  const [formData, setFormData] = useState({
    code: '',
    name: '',
    capacity: 0,
    professor: '',
    day: '',
    time: '',
    location: '',
    units: 1,
  })
  const [errors, setErrors] = useState({})

  useEffect(() => {
    if (course) {
      setFormData({
        code: course.code || '',
        name: course.name || '',
        capacity: course.capacity || 0,
        professor: course.professor || '',
        day: course.day || '',
        time: course.time || '',
        location: course.location || '',
        units: course.units || 1,
      })
    } else {
      setFormData({
        code: '',
        name: '',
        capacity: 0,
        professor: '',
        day: '',
        time: '',
        location: '',
        units: 1,
      })
    }
    setErrors({})
  }, [course])

  const validate = () => {
    const newErrors = {}

    if (!formData.code.trim()) {
      newErrors.code = 'کد درس الزامی است'
    } else if (formData.code.length < 2 || formData.code.length > 7) {
      newErrors.code = 'کد درس باید بین 2 تا 7 کاراکتر باشد'
    } else if (!/^\d+$/.test(formData.code)) {
      newErrors.code = 'کد درس باید فقط شامل اعداد باشد'
    }

    if (!formData.name.trim()) {
      newErrors.name = 'نام درس الزامی است'
    }

    if (formData.capacity < 0) {
      newErrors.capacity = 'ظرفیت نمی‌تواند منفی باشد'
    }

    if (formData.units && ![1, 2, 3].includes(parseInt(formData.units))) {
      newErrors.units = 'تعداد واحد باید 1، 2 یا 3 باشد'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (validate()) {
      onSave(formData)
    }
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: name === 'capacity' || name === 'units' ? parseInt(value) || 0 : value
    }))
    // پاک کردن خطا هنگام تغییر
    if (errors[name]) {
      setErrors(prev => {
        const newErrors = { ...prev }
        delete newErrors[name]
        return newErrors
      })
    }
  }

  const days = ['شنبه', 'یکشنبه', 'دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنج‌شنبه', 'جمعه']

  return (
    <div className="fixed inset-0 bg-black bg-opacity-70 backdrop-blur-md flex items-center justify-center z-50 p-4 animate-fade-in" onClick={onClose}>
      <div className="bg-white rounded-3xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto transform transition-all border-2 border-blue-100" onClick={(e) => e.stopPropagation()}>
        <div className="p-6 border-b-2 border-blue-100 bg-gradient-to-r from-blue-50 via-indigo-50 to-purple-50">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-4">
              <div className="flex items-center justify-center w-12 h-12 bg-gradient-to-br from-blue-600 via-blue-500 to-indigo-600 rounded-xl shadow-lg">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  {course ? (
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  ) : (
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M12 4v16m8-8H4" />
                  )}
                </svg>
              </div>
              <h2 className="text-3xl font-extrabold bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 bg-clip-text text-transparent">
                {course ? 'ویرایش درس' : 'افزودن درس جدید'}
              </h2>
            </div>
            <button
              onClick={onClose}
              className="p-2 rounded-xl text-gray-400 hover:text-gray-600 hover:bg-white transition-all duration-200 shadow-sm hover:shadow-md"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* کد درس */}
            <div>
              <label htmlFor="code" className="block text-sm font-medium text-gray-700 mb-2">
                کد درس <span className="text-red-500">*</span>
              </label>
              <input
                id="code"
                name="code"
                type="text"
                value={formData.code}
                onChange={handleChange}
                className={`input-field ${errors.code ? 'border-red-500' : ''}`}
                placeholder="مثال: 123456"
                required
              />
              {errors.code && (
                <p className="mt-1 text-sm text-red-600">{errors.code}</p>
              )}
            </div>

            {/* نام درس */}
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">
                نام درس <span className="text-red-500">*</span>
              </label>
              <input
                id="name"
                name="name"
                type="text"
                value={formData.name}
                onChange={handleChange}
                className={`input-field ${errors.name ? 'border-red-500' : ''}`}
                placeholder="مثال: پایگاه داده"
                required
              />
              {errors.name && (
                <p className="mt-1 text-sm text-red-600">{errors.name}</p>
              )}
            </div>

            {/* استاد */}
            <div>
              <label htmlFor="professor" className="block text-sm font-medium text-gray-700 mb-2">
                استاد
              </label>
              <input
                id="professor"
                name="professor"
                type="text"
                value={formData.professor}
                onChange={handleChange}
                className="input-field"
                placeholder="مثال: دکتر احمدی"
              />
            </div>

            {/* روز */}
            <div>
              <label htmlFor="day" className="block text-sm font-medium text-gray-700 mb-2">
                روز
              </label>
              <select
                id="day"
                name="day"
                value={formData.day}
                onChange={handleChange}
                className="input-field"
              >
                <option value="">انتخاب کنید</option>
                {days.map(day => (
                  <option key={day} value={day}>{day}</option>
                ))}
              </select>
            </div>

            {/* ساعت */}
            <div>
              <label htmlFor="time" className="block text-sm font-medium text-gray-700 mb-2">
                ساعت
              </label>
              <input
                id="time"
                name="time"
                type="text"
                value={formData.time}
                onChange={handleChange}
                className="input-field"
                placeholder="مثال: 8-10"
              />
            </div>

            {/* مکان */}
            <div>
              <label htmlFor="location" className="block text-sm font-medium text-gray-700 mb-2">
                مکان
              </label>
              <input
                id="location"
                name="location"
                type="text"
                value={formData.location}
                onChange={handleChange}
                className="input-field"
                placeholder="مثال: کلاس 101"
              />
            </div>

            {/* ظرفیت */}
            <div>
              <label htmlFor="capacity" className="block text-sm font-medium text-gray-700 mb-2">
                ظرفیت
              </label>
              <input
                id="capacity"
                name="capacity"
                type="number"
                min="0"
                value={formData.capacity}
                onChange={handleChange}
                className={`input-field ${errors.capacity ? 'border-red-500' : ''}`}
              />
              {errors.capacity && (
                <p className="mt-1 text-sm text-red-600">{errors.capacity}</p>
              )}
            </div>

            {/* واحد */}
            <div>
              <label htmlFor="units" className="block text-sm font-medium text-gray-700 mb-2">
                واحد
              </label>
              <select
                id="units"
                name="units"
                value={formData.units}
                onChange={handleChange}
                className={`input-field ${errors.units ? 'border-red-500' : ''}`}
              >
                <option value={1}>1 واحد</option>
                <option value={2}>2 واحد</option>
                <option value={3}>3 واحد</option>
              </select>
              {errors.units && (
                <p className="mt-1 text-sm text-red-600">{errors.units}</p>
              )}
            </div>
          </div>

          {/* Buttons */}
          <div className="flex justify-end gap-4 pt-6 border-t-2 border-gray-200">
            <button
              type="button"
              onClick={onClose}
              className="btn-secondary flex items-center gap-2 font-semibold"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M6 18L18 6M6 6l12 12" />
              </svg>
              <span>انصراف</span>
            </button>
            <button
              type="submit"
              className="btn-primary flex items-center gap-2 font-bold text-lg px-8"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
              </svg>
              <span>{course ? 'ذخیره تغییرات' : 'افزودن درس'}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default CourseModal


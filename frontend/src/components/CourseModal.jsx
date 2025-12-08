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
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4" onClick={onClose}>
      <div className="bg-white rounded-xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto" onClick={(e) => e.stopPropagation()}>
        <div className="p-6 border-b border-gray-200">
          <div className="flex justify-between items-center">
            <h2 className="text-2xl font-bold text-gray-800">
              {course ? 'ویرایش درس' : 'افزودن درس جدید'}
            </h2>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600 transition-colors"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
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
          <div className="flex justify-end gap-4 pt-4 border-t border-gray-200">
            <button
              type="button"
              onClick={onClose}
              className="btn-secondary"
            >
              انصراف
            </button>
            <button
              type="submit"
              className="btn-primary"
            >
              {course ? 'ذخیره تغییرات' : 'افزودن درس'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default CourseModal


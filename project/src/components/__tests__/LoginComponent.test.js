import { mount } from '@vue/test-utils'
import { vi } from 'vitest'
import LoginComponent from '@/components/LoginComponent.vue'
import { createRouter, createWebHistory } from 'vue-router'
import { API_BASE_URL } from '@/config.js'

describe('LoginComponent.vue', () => {
  let router

  beforeEach(() => {
    router = createRouter({
      history: createWebHistory(),
      routes: [
        { path: '/', name: 'home', component: { template: '<div>Home</div>' } },
        { path: '/admin', name: 'admin', component: { template: '<div>Admin</div>' } }
      ],
    })

    vi.spyOn(router, 'push').mockImplementation(() => {})
  })

  it('verstuurt login en navigeert bij succes', async () => {
    // Mock fetch
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ access_token: 'mock_token' })
    })

    const wrapper = mount(LoginComponent, {
      global: {
        plugins: [router],
      },
    })

    await wrapper.find('input[type="email"]').setValue('test@example.com')
    await wrapper.find('input[type="password"]').setValue('password123')

    await wrapper.find('form').trigger('submit.prevent')

    expect(fetch).toHaveBeenCalledWith(
      `${API_BASE_URL}/login`,
      expect.objectContaining({
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: 'test@example.com', password: 'password123' })
      })
    )

    expect(localStorage.getItem('token')).toBe('mock_token')
    expect(localStorage.getItem('adminEmail')).toBe('test@example.com')
    expect(router.push).toHaveBeenCalledWith('/admin')
  })

  it('toont alert bij mislukte login', async () => {
    global.fetch = vi.fn().mockResolvedValue({ ok: false })

    global.alert = vi.fn()

    const wrapper = mount(LoginComponent, {
      global: {
        plugins: [router],
      },
    })

    await wrapper.find('input[type="email"]').setValue('fout@example.com')
    await wrapper.find('input[type="password"]').setValue('verkeerd')

    await wrapper.find('form').trigger('submit.prevent')

    expect(global.alert).toHaveBeenCalledWith('Invalid credentials or session expired')
  })

  it('navigatie naar home bij klikken op Close-knop', async () => {
    const wrapper = mount(LoginComponent, {
      global: {
        plugins: [router],
      },
    })

    await wrapper.find('button[type="button"]').trigger('click')

    expect(router.push).toHaveBeenCalledWith('/')
  })

  it('voegt class `active-submit` toe als formulier is ingevuld', async () => {
    const wrapper = mount(LoginComponent, {
      global: {
        plugins: [router],
      },
    })

    const submitButton = wrapper.find('.formSubmit')
    expect(submitButton.classes()).not.toContain('active-submit')

    await wrapper.find('input[type="email"]').setValue('gebruiker@test.nl')
    await wrapper.find('input[type="password"]').setValue('geheim')

    expect(submitButton.classes()).toContain('active-submit')
  })
})

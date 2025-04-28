// AdminPanel.test.js
import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeAll, afterAll, beforeEach } from 'vitest'
import AdminPanel from '@/components/AdminPanel.vue'

const dummyRouter = { push: vi.fn() }

vi.mock('vue-router', () => ({
  useRouter: () => dummyRouter,
  RouterLink: { template: '<div><slot /></div>' },
  RouterView: { template: '<div><slot /></div>' }
}))

describe('AdminPanel.vue)', () => {
  beforeEach(() => {
    dummyRouter.push.mockReset()
    localStorage.clear()
    window.alert = vi.fn()
  })

  beforeAll(() => {
    vi.spyOn(console, 'error').mockImplementation(() => {})
  })
  
  afterAll(() => {
    console.error.mockRestore()
  })
  

  it('toont de login modal bij initialisatie', () => {
    const wrapper = mount(AdminPanel)
    expect(wrapper.find('.modal').exists()).toBe(true)
  })

  it('verbergt de modal bij succesvolle login en navigeert naar /admin', async () => {
    const wrapper = mount(AdminPanel)

    await wrapper.find('input[type="email"]').setValue('admin@gmail.com')
    await wrapper.find('input[type="password"]').setValue('admin')
    await wrapper.find('form').trigger('submit.prevent')

    expect(wrapper.vm.showModal).toBe(false)
    expect(dummyRouter.push).toHaveBeenCalledWith('/admin')
  })

  it('toont een alert en houdt de modal zichtbaar bij onjuiste login-gegevens', async () => {
    const wrapper = mount(AdminPanel)

    await wrapper.find('input[type="email"]').setValue('wrong@example.com')
    await wrapper.find('input[type="password"]').setValue('wrong')
    await wrapper.find('form').trigger('submit.prevent')

    expect(window.alert).toHaveBeenCalledWith('Invalid credentials')
    expect(wrapper.vm.showModal).toBe(true)
  })

  it('logout verwijdert de token uit localStorage en roept router.push("/") aan', async () => {
    localStorage.setItem('userToken', 'dummy')
    const wrapper = mount(AdminPanel)
  
    // Simuleer succesvolle login zodat de admin panel zichtbaar is
    await wrapper.find('input[type="email"]').setValue('admin@gmail.com')
    await wrapper.find('input[type="password"]').setValue('admin')
    await wrapper.find('form').trigger('submit.prevent')
  
    // Nu bestaat de logout knop
    const logoutBtn = wrapper.find('button.logout')  // specifiek via class 'logout' zoeken
    expect(logoutBtn.exists()).toBe(true)
  
    await logoutBtn.trigger('click')
  
    expect(localStorage.getItem('userToken')).toBe(null)
    expect(dummyRouter.push).toHaveBeenCalledWith('/')
  })
})

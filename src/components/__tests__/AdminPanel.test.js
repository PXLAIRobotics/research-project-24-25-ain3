import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import AdminPanel from '@/components/AdminPanel.vue'

const dummyRouter = { push: vi.fn() }

vi.mock('vue-router', () => ({
  useRouter: () => dummyRouter,
}))

describe('AdminPanel.vue', () => {
  beforeEach(() => {
    dummyRouter.push.mockReset()
    localStorage.clear()
  })

  it('redirects naar login als token of adminEmail ontbreekt', () => {
    mount(AdminPanel)
    expect(dummyRouter.push).toHaveBeenCalledWith('/')
  })

  it('toont dashboard componenten als alles in localStorage staat', async () => {
    localStorage.setItem('token', 'dummy')
    localStorage.setItem('adminEmail', 'admin@example.com')
    const wrapper = mount(AdminPanel)

    expect(wrapper.html()).toContain('Dashboard')
    expect(wrapper.findComponent({ name: 'UsersComponent' }).exists()).toBe(true)
    expect(wrapper.findComponent({ name: 'SettingsComponent' }).exists()).toBe(true)
    expect(wrapper.findComponent({ name: 'LogsComponent' }).exists()).toBe(true)
    expect(wrapper.findComponent({ name: 'addeventsComponent' }).exists()).toBe(true)
  })

  it('wisselt naar andere panels bij klikken op sidebar-buttons', async () => {
    localStorage.setItem('token', 'dummy')
    localStorage.setItem('adminEmail', 'admin@example.com')
    const wrapper = mount(AdminPanel)

    const buttons = wrapper.findAll('.sidebar button')
    const panels = [
      'dashboard',
      'users',
      'settings',
      'all_events',
      'event adder',
      'logs',
    ]

    for (let i = 0; i < panels.length; i++) {
      await buttons[i].trigger('click')
      expect(wrapper.vm.activePanel).toBe(panels[i])
    }
  })

  it('logout verwijdert items uit localStorage en redirect', async () => {
    localStorage.setItem('token', 'dummy')
    localStorage.setItem('adminEmail', 'admin@example.com')

    const wrapper = mount(AdminPanel)
    const logoutBtn = wrapper.find('button.logout')
    expect(logoutBtn.exists()).toBe(true)

    await logoutBtn.trigger('click')
    expect(localStorage.getItem('token')).toBe(null)
    expect(localStorage.getItem('adminEmail')).toBe(null)
    expect(dummyRouter.push).toHaveBeenCalledWith('/')
  })

  it('klikken op het logo navigeert naar interfaceComponent route', async () => {
    localStorage.setItem('token', 'dummy')
    localStorage.setItem('adminEmail', 'admin@example.com')

    const wrapper = mount(AdminPanel)
    const logo = wrapper.find('img.header-logo')
    await logo.trigger('click')

    expect(dummyRouter.push).toHaveBeenCalledWith({ name: 'interfaceComponent' })
  })
})

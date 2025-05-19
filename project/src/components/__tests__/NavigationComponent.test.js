import { mount } from '@vue/test-utils'
import { createRouter, createWebHistory } from 'vue-router'
import { vi, describe, beforeEach, it, expect } from 'vitest'
import NavigationComponent from '@/components/NavigationComponent.vue'
import { useNavList } from '@/stores/navList'
import NavigationItem from '@/components/NavigationItem.vue'

// Mock de store
vi.mock('@/stores/navList', () => ({
  useNavList: vi.fn().mockReturnValue({
    conversations: {
      1: { id: 1, name: 'Conversation 1' },
      2: { id: 2, name: 'Conversation 2' },
    },
  }),
}))

describe('NavigationComponent', () => {
  let router

  beforeEach(() => {
    router = createRouter({
      history: createWebHistory(),
      routes: [
        {
          path: '/login',
          name: 'loginComponent',
          component: { template: '<div>Login</div>' },
        },
      ],
    })

    vi.spyOn(router, 'push').mockImplementation(() => {})
  })

  it('moet router.push aanroepen bij klikken op de VIBE-knop', async () => {
    const wrapper = mount(NavigationComponent, {
      global: {
        plugins: [router],
      },
    })

    await wrapper.find('.vibe').trigger('click')

    expect(router.push).toHaveBeenCalledWith({ name: 'loginComponent' })
  })

  it('toont alle faq via NavigationItem componenten', () => {
    const wrapper = mount(NavigationComponent, {
      global: {
        plugins: [router],
      },
    })

    const items = wrapper.findAllComponents(NavigationItem)
    expect(items).toHaveLength(2)
  })
})

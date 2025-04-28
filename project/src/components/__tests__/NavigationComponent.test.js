import { mount } from '@vue/test-utils'
import { createRouter, createWebHistory } from 'vue-router'
import { vi } from 'vitest'
import NavigationComponent from '@/components/NavigationComponent.vue'
import { useNavList } from '@/stores/navList'

vi.mock('@/stores/navList', () => ({
    useNavList: vi.fn().mockReturnValue({
      conversations: {
        1: { id: 1, name: 'Conversation 1' },
        2: { id: 2, name: 'Conversation 2' },
      },
    }),
  }))
  
  describe('NavigationComponent', () => {
    let router;
  
    beforeEach(() => {
      router = createRouter({
        history: createWebHistory(),
        routes: [
          {
            path: '/admin',
            name: 'adminComponent',
            component: { template: '<div></div>' },
          },
        ],
      })
  
      vi.spyOn(router, 'push').mockImplementation(() => {});
    })
  
    it('moet router.push aanroepen wanneer op de admin-knop wordt geklikt', async () => {
      const wrapper = mount(NavigationComponent, {
        global: {
          plugins: [router],
        },
      })
    
      // Zoek de 'vibe' class of gebruik de juiste selector
      await wrapper.find('.vibe').trigger('click')
    
      expect(router.push).toHaveBeenCalledWith({ name: 'adminComponent' })
    })
  
    it('moet de lijst van gesprekken weergeven', async () => {
      const wrapper = mount(NavigationComponent, {
        global: {
          plugins: [router],
        },
      })
  
      expect(wrapper.findAllComponents({ name: 'NavigationItem' }).length).toBe(2)
    })
  })
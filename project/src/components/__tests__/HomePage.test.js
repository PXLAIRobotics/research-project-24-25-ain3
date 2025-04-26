import { mount } from '@vue/test-utils';
import { createRouter, createWebHistory } from 'vue-router';
import { vi } from 'vitest';
import HomePageComponent from '@/components/homePage.vue'; 

describe('HomePageComponent', () => {
  let router;

  beforeEach(() => {
    router = createRouter({
      history: createWebHistory(),
      routes: [
        {
          path: '/interface', 
          name: 'interfaceComponent',
          component: { template: '<div></div>' },  
        },
      ],
    });

    vi.spyOn(router, 'push').mockImplementation(() => {});
  });

  it('moet router.push aanroepen bij klikken op de afbeelding', async () => {
    const wrapper = mount(HomePageComponent, {
      global: {
        plugins: [router], 
      },
    });

    await wrapper.find('.clickable-image').trigger('click');

    expect(router.push).toHaveBeenCalledWith({ name: 'interfaceComponent' });
  });
});

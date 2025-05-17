import { mount } from '@vue/test-utils';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { createPinia } from 'pinia';  // Importeren van Pinia
import ChatComponent from '@/components/ChatComponent.vue';
import axios from 'axios';

vi.mock('axios');

describe('ChatComponent', () => {
  let pinia;

  beforeEach(() => {
    // Maak een nieuwe Pinia instantie voor elke test
    pinia = createPinia();

    // Standaard succesvolle mock implementatie in voor axios.get
    axios.get.mockResolvedValue({ data: { data: 'Mock response' } });
  });

  it('voegt een bericht toe aan de lijst wanneer de gebruiker een bericht verstuurt', async () => {
    const wrapper = mount(ChatComponent, {
      global: {
        plugins: [pinia],  // Voeg Pinia als plugin toe aan de test
      },
    });
    const input = wrapper.find('input');

    await input.setValue('Hallo');
    await input.trigger('keyup.enter');

    expect(wrapper.vm.messages).toContainEqual({ sender: 'client', message: 'Hallo' });
  });

  it('verandert de GIF correct tijdens de transitie', async () => {
    const wrapper = mount(ChatComponent, {
      global: {
        plugins: [pinia],  // Voeg Pinia als plugin toe aan de test
      },
    });
    const input = wrapper.find('input');

    await input.setValue('Test bericht');
    await input.trigger('keyup.enter');

    expect(wrapper.vm.currentGif).toBe(wrapper.vm.transitionGif);
    
    await new Promise((resolve) => setTimeout(resolve, wrapper.vm.transitionDuration));
    
    expect(wrapper.vm.currentGif).toBe(wrapper.vm.thinkingGif);
  });

  it('toont een foutmelding als de API faalt', async () => {
    axios.get.mockRejectedValue(new Error('Netwerkfout'));

    const wrapper = mount(ChatComponent, {
      global: {
        plugins: [pinia],  // Voeg Pinia als plugin toe aan de test
      },
    });
    const input = wrapper.find('input');

    await input.setValue('Test bericht');
    await input.trigger('keyup.enter');

    await new Promise((resolve) => setTimeout(resolve, 10));

    expect(wrapper.vm.messages).toContainEqual({
      sender: 'chatbot',
      message: 'Er is een fout opgetreden. Probeer het later opnieuw.'
    });
  });
});

import { render, screen } from '@testing-library/vue';
import { describe, it, expect } from 'vitest';
import HelloWorld from '../src/components/HelloWorld.vue';
import '@testing-library/jest-dom';

describe('HelloWorld.vue', () => {
  it('renders the correct message', () => {
    // Render the component with props
    render(HelloWorld, {
      props: { msg: 'Hello Vitest' },
    });

    // Assert that the message is in the document
    expect(screen.getByText('Hello Vitest')).toBeInTheDocument();
  });

  it('renders a default message when no props are passed', () => {
    render(HelloWorld);

    expect(screen.getByText('Welcome to Vue 3 + TypeScript!')).toBeInTheDocument();
  });
});

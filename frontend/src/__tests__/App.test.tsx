import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import App from '../App';
import React from 'react';

describe('App', () => {
  it('renders the header title', () => {
    render(<App />);
    expect(screen.getByText(/AI Reel Gen/i)).toBeInTheDocument();
  });

  it('renders the new project button when no project is active', () => {
    render(<App />);
    expect(screen.getByRole('button', { name: /New Project/i })).toBeInTheDocument();
  });
});

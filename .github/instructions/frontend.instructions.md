---
applyTo:
  - "**/src/components/**"
  - "**/src/pages/**"
  - "**/src/views/**"
  - "**/src/app/**"
  - "**/*.vue"
  - "**/*.svelte"
  - "**/styles/**"
  - "**/*.css"
  - "**/*.scss"
  - "**/*.less"
excludeAgent:
  - "code-review"  # Remove this line to enable for code review
---

# Frontend Development Standards

## Core Principles
- Mobile-first responsive design
- Accessibility (WCAG 2.1 AA) as a requirement, not an afterthought
- Performance budgets for bundle size and load time
- Component-driven architecture

## Component Architecture

### DO: Create small, focused components
```tsx
// ✅ Good - Single responsibility
const UserAvatar: React.FC<UserAvatarProps> = ({ user, size = 'md' }) => (
  <img
    src={user.avatarUrl}
    alt={`${user.name}'s avatar`}
    className={cn('rounded-full', sizeClasses[size])}
  />
);

const UserName: React.FC<UserNameProps> = ({ user }) => (
  <span className="font-medium text-gray-900">{user.name}</span>
);

// Compose into larger components
const UserCard: React.FC<UserCardProps> = ({ user }) => (
  <div className="flex items-center gap-3">
    <UserAvatar user={user} />
    <UserName user={user} />
  </div>
);
```

### DON'T: Create monolithic components
```tsx
// ❌ Avoid - Too many responsibilities
const UserSection = ({ users, onEdit, onDelete, filter, sort, ...props }) => {
  // 500+ lines of mixed concerns
};
```

## State Management

### Use appropriate state location
| State Type | Location | Example |
|------------|----------|---------|
| Local UI | useState | Form input, dropdown open |
| Shared UI | Context | Theme, sidebar open |
| Server | React Query/SWR | User data, products |
| Global app | Zustand/Redux | Auth, cart |

### DO: Colocate state with usage
```tsx
// State lives close to where it's used
const SearchFilter: React.FC = () => {
  const [query, setQuery] = useState('');
  const [isOpen, setIsOpen] = useState(false);
  
  return (
    <div>
      <input value={query} onChange={e => setQuery(e.target.value)} />
      {/* ... */}
    </div>
  );
};
```

## Accessibility

### Required for all interactive elements
```tsx
// Buttons
<button
  type="button"
  onClick={handleClick}
  aria-label="Close dialog"  // If no visible text
  disabled={isLoading}
>
  <CloseIcon aria-hidden="true" />
</button>

// Forms
<label htmlFor="email">Email address</label>
<input
  id="email"
  type="email"
  aria-describedby="email-error"
  aria-invalid={hasError}
/>
{hasError && <p id="email-error" role="alert">{error}</p>}

// Keyboard navigation
<div
  role="listbox"
  tabIndex={0}
  onKeyDown={handleKeyDown}
  aria-activedescendant={activeId}
>
```

### Use semantic HTML
```tsx
// ✅ Prefer
<nav aria-label="Main navigation">
<main>
<article>
<aside>
<header>
<footer>
<button>
<a href="/page">

// ❌ Avoid
<div onclick="...">
<span class="link">
```

## CSS & Styling

### Use design tokens
```css
:root {
  /* Colors */
  --color-primary-500: #3b82f6;
  --color-gray-100: #f3f4f6;
  
  /* Spacing */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-4: 1rem;
  
  /* Typography */
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --line-height-normal: 1.5;
  
  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
}
```

### Mobile-first responsive design
```css
/* Base styles for mobile */
.card {
  padding: var(--space-4);
  display: flex;
  flex-direction: column;
}

/* Tablet and up */
@media (min-width: 768px) {
  .card {
    flex-direction: row;
    padding: var(--space-6);
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .card {
    padding: var(--space-8);
  }
}
```

### Use Tailwind CSS utilities effectively
```tsx
// ✅ Group related utilities
<div className={cn(
  // Layout
  'flex items-center gap-4',
  // Spacing
  'p-4 md:p-6',
  // Colors
  'bg-white dark:bg-gray-800',
  // Border
  'rounded-lg border border-gray-200',
  // Interactive
  'hover:shadow-md transition-shadow',
  // Conditional
  isActive && 'ring-2 ring-primary-500'
)}>
```

## Performance

### Optimize bundle size
```tsx
// Lazy load routes and heavy components
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Chart = lazy(() => import('./components/Chart'));

// Tree-shakeable imports
import { Button } from '@/components/ui/button';  // ✅
import * as UI from '@/components/ui';  // ❌ Imports everything
```

### Optimize images
```tsx
// Use next/image or similar
<Image
  src="/hero.jpg"
  alt="Hero image"
  width={1200}
  height={600}
  priority  // For above-the-fold images
  sizes="(max-width: 768px) 100vw, 1200px"
/>

// Use appropriate formats
<picture>
  <source srcSet="/image.avif" type="image/avif" />
  <source srcSet="/image.webp" type="image/webp" />
  <img src="/image.jpg" alt="Description" loading="lazy" />
</picture>
```

### Memoize expensive operations
```tsx
// Memoize expensive computations
const sortedItems = useMemo(
  () => items.slice().sort((a, b) => b.date - a.date),
  [items]
);

// Memoize callbacks for child components
const handleSubmit = useCallback(
  (data: FormData) => {
    mutation.mutate(data);
  },
  [mutation]
);

// Memoize components that receive object/array props
const MemoizedList = memo(ItemList);
```

## Forms

### Use form libraries for complex forms
```tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

const schema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
});

const LoginForm: React.FC = () => {
  const { register, handleSubmit, formState: { errors } } = useForm({
    resolver: zodResolver(schema),
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('email')} aria-invalid={!!errors.email} />
      {errors.email && <p role="alert">{errors.email.message}</p>}
      {/* ... */}
    </form>
  );
};
```

## Error Handling

### Implement error boundaries
```tsx
class ErrorBoundary extends Component<Props, State> {
  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    logger.error('UI Error', { error, componentStack: info.componentStack });
  }

  render() {
    if (this.state.hasError) {
      return <ErrorFallback error={this.state.error} onRetry={this.reset} />;
    }
    return this.props.children;
  }
}
```

### Handle loading and error states
```tsx
const UserProfile: React.FC<{ userId: string }> = ({ userId }) => {
  const { data: user, isLoading, error } = useQuery(['user', userId], fetchUser);

  if (isLoading) return <ProfileSkeleton />;
  if (error) return <ErrorMessage error={error} />;
  if (!user) return <NotFound />;

  return <Profile user={user} />;
};
```

## Testing

### Test user behavior, not implementation
```tsx
import { render, screen, userEvent } from '@testing-library/react';

test('submits form with user data', async () => {
  const onSubmit = vi.fn();
  render(<LoginForm onSubmit={onSubmit} />);

  await userEvent.type(screen.getByLabelText(/email/i), 'user@example.com');
  await userEvent.type(screen.getByLabelText(/password/i), 'password123');
  await userEvent.click(screen.getByRole('button', { name: /sign in/i }));

  expect(onSubmit).toHaveBeenCalledWith({
    email: 'user@example.com',
    password: 'password123',
  });
});
```

## File Organization
```
src/
├── components/
│   ├── ui/                 # Primitive components (Button, Input)
│   ├── features/           # Feature-specific components
│   └── layouts/            # Layout components
├── hooks/                  # Custom hooks
├── lib/                    # Utilities and helpers
├── styles/                 # Global styles
└── pages/ or app/          # Route components
```

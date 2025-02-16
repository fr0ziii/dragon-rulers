# UI Guidelines

This document outlines the guidelines and patterns used for building the UI in the `src/ui` directory.

## Component Library

The project primarily uses **Shadcn UI** (`shadcn/ui`) for building UI components. Shadcn UI provides a collection of reusable components built on top of Radix UI and styled with Tailwind CSS.

*   **Configuration:** The Shadcn UI configuration is located in `components.json`.
*   **Style:** The "new-york" style is used.
*   **React Server Components:** The project uses React Server Components (`rsc: true`).
*   **TypeScript:** TypeScript is used throughout the project (`tsx: true`).

## Styling

### Tailwind CSS

*   **Framework:** Tailwind CSS is the primary styling framework.
*   **Configuration:** The Tailwind configuration file is `tailwind.config.ts`.
*   **Base Color:** The base color is set to "neutral".
*   **CSS Variables:** CSS variables are used extensively for colors and border-radius. These are defined in `src/app/globals.css`.
*   **Prefix:** No prefix is used for Tailwind classes (`prefix: ""`).
*   **Plugins:** The `tailwindcss-animate` plugin is used for animations.
* **Base Styles:** Tailwind's base styles are included using `@tailwind base` in `globals.css`.
* **Components Styles:** Tailwind's component styles are included using `@tailwind components` in `globals.css`.
* **Utility Styles:** Tailwind's utility styles are included using `@tailwind utilities` in `globals.css`.

### PostCSS

*   **Configuration:** PostCSS is configured in `postcss.config.mjs`.
*   **Plugins:** The `tailwindcss` plugin is used to process Tailwind CSS.

### CSS Variables

CSS variables are defined in `src/app/globals.css` within the `:root` (light theme) and `.dark` (dark theme) selectors. They follow a consistent naming convention:

```css
:root {
  --background: 0 0% 100%;
  --foreground: 0 0% 3.9%;
  /* ... other variables ... */
}
```

### Class Variance Authority (CVA)

The `class-variance-authority` library is used to define style variants for some components (e.g., `Button`, `SidebarMenuButton`). This allows for creating reusable components with different styles based on props.

### `cn` Utility

The `cn` utility function (likely from `clsx` or a similar library, located in `@/lib/utils`) is used to conditionally apply class names. This is a common pattern for combining Tailwind classes with dynamic styles.

## Component Structure

*   **Functional Components:** Components are primarily functional components, often using `React.forwardRef` to allow passing refs.
*   **Radix UI:** Many components are built on top of Radix UI primitives (e.g., `Avatar`, `Tooltip`, `Sheet`, `Collapsible`). These provide headless UI components with accessibility features.
*   **Composition:** Complex components are often composed of smaller, reusable sub-components (e.g., `Sidebar` is composed of `SidebarHeader`, `SidebarContent`, `SidebarMenu`, etc.).
*   **Context API:** The Context API is used for managing state that needs to be shared across multiple components (e.g., `SidebarContext`).
*   **Custom Hooks:** Custom hooks are used to encapsulate logic (e.g., `useSidebar`, `useIsMobile`).
*   **Slots:** The `@radix-ui/react-slot` component is used to create flexible components that can accept different child elements.
* **Data Attributes:** Data attributes are used extensively to manage styles and behavior based on component state.

## File and Folder Structure

*   **`src/app`:** Contains the main application logic, including pages and layouts.
*   **`src/components`:** Contains reusable UI components.
    *   **`src/components/ui`:** Contains base UI components, often styled with Tailwind CSS and built on top of Radix UI.
*   **`src/lib`:** Contains utility functions and shared logic.
*   **`src/hooks`:** Contains custom React hooks.
*   **`models`:** Contains data models.
*   **`public`:** Contains static assets.

## Naming Conventions

*   **Components:** PascalCase (e.g., `Sidebar`, `Button`, `AvatarImage`).
*   **Files:** kebab-case (e.g., `app-sidebar.tsx`, `button.tsx`).
*   **CSS Variables:** kebab-case with a double hyphen prefix (e.g., `--background`, `--primary-foreground`).
*   **Data Attributes:** `data-[component-name]` or `data-[state]` (e.g., `data-sidebar`, `data-state`).

## Aliases
Path aliases are defined to simplify imports:
* `@/components`: `src/components`
* `@/lib/utils`: `src/lib/utils`
* `@/components/ui`: `src/components/ui`
* `@/lib`: `src/lib`
* `@/hooks`: `src/hooks`

## TypeScript

*   TypeScript is used throughout the project.
*   Interfaces and types are defined for component props.

## Accessibility

*   ARIA attributes are used where appropriate.
*   Radix UI primitives, which are designed with accessibility in mind, are used extensively.
*   `SidebarTrigger` uses `aria-label` and `sr-only` for screen readers.

## Other

* **Icon Library**: Lucide React
* **Mobile Responsiveness:** The `useIsMobile` hook is used to detect mobile devices and adjust the UI accordingly.
* **Cookie Storage:** Cookies are used to persist the sidebar state.
* **Keyboard Shortcuts:** Keyboard shortcuts are used to improve user experience (e.g., Cmd/Ctrl + B to toggle the sidebar).
* **Skeleton Components:** It includes a `SidebarMenuSkeleton` component for loading states.
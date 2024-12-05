# Stratagem Hell

Stratagem Hell is a TypeScript-based gaming application with the following features:

## Overview

The game splits the screen into two halves:

1. **Top Half (Dashboard):**

    - Displays:
        - The current score.
        - Remaining time.
        - A preview of the next combo to be performed.

2. **Bottom Half (Comboter):**
    - Displays:
        - The current combo, represented as arrows for each key the user needs to press (e.g., `←`, `→`, `↑`, `↓`).
        - Feedback for each key press:
            - **Green** for correct presses.
            - **Red** for incorrect presses (with a shake animation).
        - Visual progression as keys are correctly pressed.
        - Automatically transitions to the next combo after completing the current one.
        - A "Game Over" screen when all combos are completed.

## Gameplay Mechanics

-   The player performs combos by pressing a series of keys:
    -   Supported keys include:
        -   Arrow keys (`ArrowLeft`, `ArrowRight`, `ArrowUp`, `ArrowDown`).
        -   Alternative keys (`Z`, `Q`, `S`, `D`).
-   Combos are represented as an array of objects (`ComboProps`) where each key has its own status:
    -   **`success`**: Key was pressed correctly.
    -   **`failed`**: Key was pressed incorrectly.
    -   **`idle`**: Key is yet to be pressed.
    -   **`loading`**: Key is the current key to be pressed.
-   The game ends when all combos have been completed. At this point:
    -   The **Game Over** screen is displayed.
    -   The player can restart the game using:
        -   A "Restart" button (with a tooltip: `"Or press [Enter]"`).
        -   The **Enter** key.

## Code Details

### File Structure

-   **`Dashboard` Component**:
    -   Displays score, time, and the next combo preview.
-   **`Comboter` Component**:
    -   Displays the current combo visually with arrows.
    -   Handles key press feedback and progression.
-   **`useCombo` Hook**:
    -   Manages the game state:
        -   Current combo and its keys' statuses.
        -   Progression through combos.
        -   Game Over state.
        -   Restart functionality.
-   **`Arrow` Component**:
    -   Displays a single arrow with dynamic styles based on its status.
-   **`RestartButton` Component**:
    -   A reusable button that restarts the game.

### Data Structures

Combos are represented with the following types:

```typescript
export type PossibleKeys = 'left' | 'right' | 'up' | 'down';
export type PossibleStatus = 'idle' | 'loading' | 'success' | 'failed';

export type Status = {
    status: PossibleStatus;
};

export type KeyProps = { key: PossibleKeys } & Status;

export type ComboProps = {
    id: number;
    name: string;
    keys: Array<KeyProps>;
} & Status;
```

### Gameplay Features

-   Keys are dynamically updated:
    -   Correct keys turn **green** (`success`).
    -   Incorrect keys turn **red** (`failed`) and shake briefly.
    -   The current key is **blue** (`loading`).
    -   Unpressed keys are **gray** (`idle`).
-   Automatically transitions to the next combo when the current combo is completed.
-   Displays "Game Over!" when all combos are completed, with a **Restart** option.

### Event Handling

-   Arrow keys and `ZQSD` keys trigger gameplay actions.
-   Pressing **Enter** restarts the game when it's over.

### Reusable Components

-   `RestartButton`:
    -   Includes a tooltip: `"Or press [Enter]"`.
    -   Styled for clarity and accessibility.

### Animation

-   Incorrect key presses shake the corresponding arrow.
-   Smooth transitions for key colors and progression.

### Component Design

-   Components are modular and reusable, following best practices for clean and maintainable code.

## Deliverables

-   Complete the **Stratagem Hell** application in TypeScript.
-   Ensure all features work as described.
-   The code should be clean, modular, and well-documented.

import React, { FunctionComponent, useEffect } from 'react';
import { Box, Typography } from '@mui/material';
import ComboShape from './ComboShape';
import RestartButton from './RestartButton';
import { ComboProps, PossibleKeys } from '../ComboObject/types';

interface ComboterProps {
    currentCombo?: ComboProps; // Optional to handle undefined
    validateKeyPress: (key: PossibleKeys) => void;
    isGameOver: boolean;
    restartGame: () => void;
}

const keyMap: Record<string, PossibleKeys> = {
    ArrowLeft: 'left',
    ArrowRight: 'right',
    ArrowUp: 'up',
    ArrowDown: 'down',
    z: 'up',
    q: 'left',
    s: 'down',
    d: 'right',
};

const Comboter: FunctionComponent<ComboterProps> = function ({
    currentCombo,
    validateKeyPress,
    isGameOver,
    restartGame,
}) {
    useEffect(() => {
        const handleKeyDown = (event: KeyboardEvent) => {
            if (isGameOver) {
                if (event.key === 'Enter') {
                    event.preventDefault();
                    restartGame();
                }
                return;
            }

            const mappedKey = keyMap[event.key.toLowerCase()];
            if (mappedKey) {
                event.preventDefault();
                console.debug(`Key pressed: ${event.key}, mapped to: ${mappedKey}`);
                validateKeyPress(mappedKey);
            }
        };

        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
    }, [validateKeyPress, isGameOver, restartGame]);

    return (
        <Box
            sx={{
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center',
                alignItems: 'center',
                width: '100%',
                height: '100%',
                padding: 2,
            }}
        >
            {isGameOver ? (
                <>
                    <Typography
                        variant="h4"
                        sx={{ mb: 2 }}
                    >
                        Game Over!
                    </Typography>
                    <RestartButton onClick={restartGame} />
                </>
            ) : (
                <ComboShape currentCombo={currentCombo} />
            )}
        </Box>
    );
};

export default Comboter;

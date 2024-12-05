import React, { FunctionComponent } from 'react';
import { Box } from '@mui/material';
import { PossibleStatus } from '../ComboObject/types';

interface ArrowProps {
    direction: 'left' | 'right' | 'up' | 'down';
    status: PossibleStatus; // Now using PossibleStatus
}

const directionToSymbol: Record<ArrowProps['direction'], string> = {
    left: '←',
    right: '→',
    up: '↑',
    down: '↓',
};

const Arrow: FunctionComponent<ArrowProps> = function ({ direction, status }) {
    const styles = React.useMemo(() => {
        const baseStyles = {
            fontSize: '3rem',
            fontWeight: 'bold',
            textAlign: 'center',
            transition: 'transform 0.2s, color 0.2s',
            '@keyframes shake': {
                '0%, 100%': { transform: 'translateX(0)' },
                '25%': { transform: 'translateX(-15px)' },
                '75%': { transform: 'translateX(15px)' },
            },
        };

        switch (status) {
            case 'success':
                return { ...baseStyles, color: 'green', transform: 'scale(1.2)' };
            case 'failed':
                return { ...baseStyles, color: 'red', animation: 'shake 0.5s ease-in-out' };
            case 'loading':
                return { ...baseStyles, color: 'blue', transform: 'scale(1.1)' };
            default:
                return { ...baseStyles, color: 'gray' };
        }
    }, [status]);

    return <Box sx={styles}>{directionToSymbol[direction]}</Box>;
};

export default Arrow;

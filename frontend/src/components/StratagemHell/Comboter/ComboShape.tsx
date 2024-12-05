import React, { FunctionComponent } from 'react';
import { Stack, Typography } from '@mui/material';
import Arrow from './Arrow';
import { ComboProps } from '../ComboObject/types';

interface ComboShapeProps {
    currentCombo?: ComboProps; // Optional to handle undefined
}

const ComboShape: FunctionComponent<ComboShapeProps> = function ({ currentCombo }) {
    if (!currentCombo) {
        // Render fallback if no currentCombo is available
        return (
            <Typography
                variant="h6"
                sx={{ textAlign: 'center', color: 'gray' }}
            >
                No combo available
            </Typography>
        );
    }

    return (
        <Stack
            direction="row"
            spacing={2}
            sx={{
                justifyContent: 'center',
                alignItems: 'center',
            }}
        >
            {currentCombo.keys.map((keyData) => (
                <Arrow
                    key={`${keyData.key}-${currentCombo.id}`}
                    direction={keyData.key}
                    status={keyData.status}
                />
            ))}
        </Stack>
    );
};

export default ComboShape;

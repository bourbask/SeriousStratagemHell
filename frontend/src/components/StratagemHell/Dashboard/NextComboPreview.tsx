import React from 'react';
import { Box, Typography, Stack } from '@mui/material';
import { PossibleKeys } from '../ComboObject/types';

interface NextComboPreviewProps {
    nextCombo: PossibleKeys[]; // The sequence of keys in the next combo
}

const keyToArrow: Record<PossibleKeys, string> = {
    left: '←',
    right: '→',
    up: '↑',
    down: '↓',
};

const NextComboPreview: React.FC<NextComboPreviewProps> = function ({ nextCombo }) {
    return (
        <Box
            sx={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'flex-end',
            }}
        >
            {/* Title */}
            <Typography
                variant="h6"
                sx={{ mb: 1 }}
            >
                Next Combo:
            </Typography>

            {/* Combo Preview */}
            <Stack
                direction="row"
                spacing={1}
            >
                {nextCombo.map((key, index) => (
                    <Typography
                        key={index}
                        variant="h5"
                        sx={{
                            fontWeight: 'bold',
                            padding: '4px 8px',
                            border: '1px solid #ddd',
                            borderRadius: '4px',
                            backgroundColor: '#f0f0f0',
                        }}
                    >
                        {keyToArrow[key]}
                    </Typography>
                ))}
            </Stack>
        </Box>
    );
};

export default NextComboPreview;

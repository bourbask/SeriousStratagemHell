// useComboGenerator.tsx

import { useEffect, useState } from 'react';
import { ComboProps, PossibleKeys, PossibleStatus } from './types';

const directions: PossibleKeys[] = ['left', 'right', 'up', 'down'];

interface ComboGeneratorParams {
    numCombos?: number;
    minComboLength?: number;
    maxComboLength?: number;
}

// Generate a random key from the available directions
const getRandomKey = (): PossibleKeys => directions[Math.floor(Math.random() * directions.length)];

// Generate a new unique identifier
const generateUuid = (): string => Math.random().toString(36).substring(2, 15);

// Custom hook to generate combos with specified parameters
const useComboGenerator = (params: ComboGeneratorParams = {}) => {
    const [combos, setCombos] = useState<Array<ComboProps>>([]);

    useEffect(() => {
        const {
            numCombos = Math.floor(Math.random() * 5) + 3, // Default between 3 and 7 combos
            minComboLength = 3,
            maxComboLength = 6,
        } = params;

        const generatedCombos: Array<ComboProps> = [];

        for (let i = 0; i < numCombos; i++) {
            const comboLength =
                Math.floor(Math.random() * (maxComboLength - minComboLength + 1)) + minComboLength;
            const keys = Array.from({ length: comboLength }, () => ({
                id: generateUuid(),
                key: getRandomKey(),
                status: 'idle' as PossibleStatus,
            }));

            generatedCombos.push({
                id: generateUuid(),
                name: `combo-${i + 1}`,
                keys,
                status: 'idle',
            });
        }

        setCombos((prevCombos) => {
            // Only set combos if they are different from the previous ones to prevent infinite loops
            const areCombosDifferent =
                JSON.stringify(prevCombos) !== JSON.stringify(generatedCombos);
            return areCombosDifferent ? generatedCombos : prevCombos;
        });
    }, [params.numCombos, params.minComboLength, params.maxComboLength]);

    return combos;
};

export default useComboGenerator;

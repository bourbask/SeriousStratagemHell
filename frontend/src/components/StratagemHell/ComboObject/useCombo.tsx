import { useCallback, useState, useEffect } from 'react';
import { ComboProps, PossibleKeys } from './types';

const useCombo = (initialCombos?: Array<ComboProps>) => {
    const [combos, setCombos] = useState<Array<ComboProps>>(initialCombos ?? []);
    const [currentComboIndex, setCurrentComboIndex] = useState(0);
    const [userProgress, setUserProgress] = useState(0);
    const [isGameOver, setIsGameOver] = useState(false);

    useEffect(() => {
        // When initialCombos changes, reset everything
        if (initialCombos) {
            setCombos(initialCombos);
            setCurrentComboIndex(0);
            setUserProgress(0);
            setIsGameOver(false);
        }
    }, [initialCombos]);

    // Handle correct key press
    const handleCorrectKey = useCallback(() => {
        setCombos((prevCombos) => {
            const updatedCombos = [...prevCombos];
            const currentCombo = updatedCombos[currentComboIndex];
            currentCombo.keys[userProgress].status = 'success';

            setUserProgress((prev) => {
                if (prev + 1 >= currentCombo.keys.length) {
                    currentCombo.status = 'success';

                    if (currentComboIndex + 1 >= updatedCombos.length) {
                        setIsGameOver(true); // No more combos
                        console.debug('Game over: No more combos available.');
                    } else {
                        // Move to the next combo
                        setCurrentComboIndex((prevIndex) => prevIndex + 1);
                        console.debug(`Moving to next combo: Index ${currentComboIndex + 1}`);
                    }
                    return 0;
                }
                return prev + 1;
            });

            return updatedCombos;
        });
    }, [currentComboIndex, userProgress]);

    // Handle incorrect key press
    const handleIncorrectKey = useCallback(() => {
        setCombos((prevCombos) => {
            const updatedCombos = [...prevCombos];
            const currentCombo = updatedCombos[currentComboIndex];
            currentCombo.keys[userProgress].status = 'failed'; // Mark key as failed
            console.debug(`Incorrect key press at userProgress: ${userProgress}`);
            return updatedCombos;
        });
    }, [currentComboIndex, userProgress]);

    // Validate key press
    const validateKeyPress = useCallback(
        (key: PossibleKeys) => {
            if (isGameOver) return;

            const currentCombo = combos[currentComboIndex];
            if (!currentCombo) return;

            const expectedKey = currentCombo.keys[userProgress];

            console.debug(`Validating key press: Expected ${expectedKey.key}, Received ${key}`);

            if (expectedKey.key === key) {
                handleCorrectKey();
            } else {
                handleIncorrectKey();
            }
        },
        [combos, currentComboIndex, userProgress, isGameOver, handleCorrectKey, handleIncorrectKey],
    );

    // Restart the game
    const restartGame = useCallback(() => {
        setCombos((prevCombos) =>
            prevCombos.map((combo) => ({
                ...combo,
                status: 'idle',
                keys: combo.keys.map((key) => ({ ...key, status: 'idle' })),
            })),
        );
        setCurrentComboIndex(0);
        setUserProgress(0);
        setIsGameOver(false);
        console.debug('Game restarted.');
    }, []);

    return {
        currentCombo: combos[currentComboIndex],
        validateKeyPress,
        isGameOver,
        restartGame,
    };
};

export default useCombo;

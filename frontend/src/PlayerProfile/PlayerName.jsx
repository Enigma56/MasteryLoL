//TODO: Add JSDoc comments for some level of type-hints
/**
 * @param {String} name - Riot profile name
 * @param {String} tag - Riot tagline
 * @param {boolean} isLoading - is name being fetched
 * @returns {JSX.Element}
 */
const PlayerName = ({name, tag, isLoading}) => {
    return (
        <>
        {isLoading ? (
            <div className="flex flex-row justify-center">
                <h1 className="underline">...</h1>
            </div>
        ) : (
            <div className="flex flex-row justify-center">
                <h1 className="underline">{name} #{tag}</h1>
            </div>
        )}
        </>
    )
}

export default PlayerName
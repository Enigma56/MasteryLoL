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
class CustomPromise extends Promise {
    constructor(executor) {
        super(executor);
    }

    static resolve() {
        return {
            then(resolve, reject) {
                Promise.resolve().then(BigInt).then(resolve, reject);
                reject();
            }
        };
    }
}

CustomPromise.any([1]);

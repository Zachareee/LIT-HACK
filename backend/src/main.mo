import HashMap "mo:base/HashMap";
import Text "mo:base/Text";
import Array "mo:base/Array";

actor class Main(prompts : [Text], choices : [[Nat]]) {
    public func getChoices(user : Text, chosenNumber : Nat) : async [Text] {
        UserStorage.put(user, choices[chosenNumber]);
        UserStorage := UserStorage;
        return Array.map<Nat, Text>(choices[chosenNumber], func idx = prompts[idx]);
    };

    public func chat(user : Text, replyIdx : Nat) : async [Text] {
        let userArr = UserStorage.get(user);
        switch (userArr) {
            case (?userArr) return await getChoices(user, (userArr[replyIdx]));
            case null return await getChoices(user, 0);
        };
    };

    var UserStorage : HashMap.HashMap<Text, [Nat]> = HashMap.HashMap<Text, [Nat]>(0, Text.equal, Text.hash);
};

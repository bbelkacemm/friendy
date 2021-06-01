class Proposition {
  String? value;

  Proposition({this.value});

  static List<Proposition> fromJson(json) {
    List<Proposition> propositions = [];
    for (var value in json['propositions'])
      propositions.add(Proposition(value: value));
    return propositions;
  }
}

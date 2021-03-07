#!/usr/bin/env bash

if [[ $# != 2 ]]; then
    echo "$0 COMMAND PATH"
    exit 1
fi

command=$1

function check {
    local target
    target=$(readlink -f "$1")
    AtomicParsley "$target" -T | grep -q "jpn"
    return $?
}

function fix {
    local target
    target="$(readlink -f "$1")"
    if ! check "$target"; then
        echo "$target has WALKMAN compatible tag"
        exit 0
    fi
    cp "$target" "$(dirname "$target")/backup_$(basename "$target")"
    local filename
    filename=$(basename "$target")
    AtomicParsley "$target" --manualAtomRemove moov.udta.albm:lang=jpn --manualAtomRemove moov.udta.cprt:lang=jpn --manualAtomRemove moov.udta.dscp:lang=jpn --manualAtomRemove moov.udta.gnre:lang=jpn --manualAtomRemove moov.udta.perf:lang=jpn --manualAtomRemove moov.udta.titl:lang=jpn -o "$(dirname "$target")/${filename%.*}_fixed.${filename##*.}"
}

if [[ $command == "check" ]]; then
    check "$2"
    code=$?
    if [[ code -eq 0 ]]; then
        echo "Should fix $2"
    fi
elif [[ $command == "fix" ]]; then
    fix "$2"
fi


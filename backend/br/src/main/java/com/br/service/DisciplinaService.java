package com.br.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.br.model.Disciplina;
import com.br.repository.DisciplinaRepository;

@Service
public class DisciplinaService {
    private final DisciplinaRepository disciplinaRepository;

    @Autowired
    public DisciplinaService(DisciplinaRepository disciplinaRepository) {
        this.disciplinaRepository = disciplinaRepository;
    }

    public List<Disciplina> getAllDisciplinas() {
        return disciplinaRepository.findAll();
    }
}

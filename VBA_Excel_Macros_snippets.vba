Sub leitura()
    x = Range("a1")
    Range("a2") = x
End Sub


Sub caixa_de_mensagem()
    MsgBox (Range("a1"))
End Sub


Sub somar_amarela()
    soma = 0
    For Each cell In Range("a5:b6")
        soma = soma + cell.Value
    Next
    
    Range("c6") = soma
End Sub


Sub contar()
    nome = Range("a8")
    Range("d8") = 0
    
    For Each cell In Range("b8:c10")
        If cell.Value = nome Then
            Range("d8") = Range("d8") + 1
        End If
    Next
End Sub


Sub contar_numeros()
    For Each question_cell In Range("a13:c13")
        question_cell.Offset(1, 0) = 0
        For Each cell In Range("a15:c18")
            If cell.Value = question_cell.Value Then
                question_cell.Offset(1, 0) = question_cell.Offset(1, 0) + 1
            End If
        Next cell
    Next question_cell
End Sub


Sub nomes()
    Range("a21") = "Ana"
    Range("a22") = "João"
    Range("a23") = "Tiago"
    Range("a24") = "Diana"
End Sub


Sub copiar_area()
    For Each cell In Range("a21:a24")
        cell.Offset(0, 1) = cell
    Next
End Sub


Sub apagar()
    For Each cell In Range("a21:b24")
        cell.ClearContents
    Next
End Sub

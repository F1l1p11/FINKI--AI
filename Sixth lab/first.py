import warnings
warnings.filterwarnings(action='ignore', category=FutureWarning)

from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

# I -> Interested
# H -> High income
# M -> Marketing
# R -> Read reviews
# B -> Browse website
# C -> Purchase
# D -> Discount

model = DiscreteBayesianNetwork([
    ('H','I'),
    ('M','I'),
    ('I','R'),
    ('I','B'),
    ('R','C'),
    ('B','C'),
    ('D','C')
])

CPD_H = TabularCPD(variable='H', variable_card=2, values=[[0.7],[0.3]])
CPD_M = TabularCPD(variable='M', variable_card=2, values=[[0.6],[0.4]])
CPD_D = TabularCPD(variable='D', variable_card=2, values=[[0.75],[0.25]])

CPD_I = TabularCPD(variable='I', variable_card=2,
    values=[
        [0.90, 0.30, 0.25, 0.05],
        [0.10, 0.70, 0.75, 0.95]],
    evidence=['H','M'],
    evidence_card=[2,2]
)

CPD_R = TabularCPD(variable='R', variable_card=2,
    values=[
        [0.80, 0.20],
        [0.20, 0.80]],
    evidence=['I'],
    evidence_card=[2]
)

CPD_B = TabularCPD(variable='B', variable_card=2,
    values=[
        [0.75, 0.15],
        [0.25, 0.85]],
    evidence=['I'],
    evidence_card=[2]
)

CPD_C = TabularCPD(variable='C', variable_card=2,
    values=[
        [0.95,0.65,0.50,0.22,0.45,0.20,0.10,0.02],
        [0.05,0.35,0.50,0.78,0.55,0.80,0.90,0.98]],
    evidence=['R','B','D'],
    evidence_card=[2,2,2]
)

model.add_cpds(CPD_H, CPD_M, CPD_D, CPD_I, CPD_R, CPD_B, CPD_C)

assert model.check_model()

infer = VariableElimination(model)

print("\nP(I=1 | B=1, M=1)")
q1 = infer.query(['I'], evidence={'B':1, 'M':1})
print(q1)

print("\nP(R=1 | I=1)")
q2 = infer.query(['R'], evidence={'I':1})
print(q2)

print("\nP(C=1 | B=1)")
q3 = infer.query(['C'], evidence={'B':1})
print(q3)

print("\nP(B=1 | I=1)")
q4 = infer.query(['B'], evidence={'I':1})
print(q4)

print("\nP(M=1 | I=1)")
q5 = infer.query(['M'], evidence={'I':1})
print(q5)

print("\nP(B=1 | C=1, R=0)")
q6 = infer.query(['B'], evidence={'C':1, 'R':0})
print(q6)